from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import connect_db, close_db
from .config import settings
from .routes import auth, tasks, career, resume, mentor, internships, stats, courses, gate


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    connect_db()
    print("[INFO] Application startup: Database connection attempt finished.")
    
    # Auto-seed if in Demo Mode (In-Memory DB)
    from .database import is_mock_mode
    if is_mock_mode():
        print("[INFO] DEMO MODE DETECTED: Auto-seeding in-memory database...")
        from . import seed_data
        # Run seeding without clearing (since it's fresh anyway) or exit
        # We need to adapt seed_data.main to be callable or call functions directly
        try:
            # We'll rely on the existing main() which clears and seeds
            # But we need to suppress the connection check exit in seed_data if we call it
            # Actually, seed_data.main() calls connect_db() again. 
            # Better to call the seed functions directly or ensure connect_db() handles re-connection gracefully.
            # Our connect_db is idempotent-ish but resets client if called.
            # Let's just call the seed functions directly to avoid reconnecting.
            
            print("[SEED] Seeding demo data...")
            seed_data.seed_career_domains()
            student_ids = seed_data.seed_students(30)
            seed_data.seed_tasks(student_ids)
            seed_data.seed_activities(student_ids)
            seed_data.seed_courses()
            seed_data.seed_internships(student_ids)
            seed_data.seed_gate_questions()
            print("[INFO] Demo data seeded successfully!")
            print("       Admin: admin@aiconsular.com / admin123")
            print("       Student: student1@example.com / password123")
        except Exception as e:
            print(f"[ERROR] Failed to seed demo data: {e}")
            
    yield
    # Shutdown
    close_db()


# Create FastAPI app
app = FastAPI(
    title="AI Consular API",
    description="Intelligent Academic & Career Guidance System for B-Tech Students",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url.rstrip('/'),
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:3000",
    ] if settings.allowed_hosts != "*" else ["*"],
    # Note: if origins is ["*"], allow_credentials must be False
    allow_credentials=True if settings.allowed_hosts != "*" else False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(career.router)
app.include_router(resume.router)
app.include_router(mentor.router)
app.include_router(internships.router)
app.include_router(stats.router)
app.include_router(courses.router)
app.include_router(gate.router)
from .routes import quiz
app.include_router(quiz.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Consular API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
