"""
Demo data seeding script for AI Consular

Run this script to populate the database with sample data:
python -m app.seed_data
"""

from faker import Faker
from datetime import datetime, timedelta
import random
import sys
from app.database import connect_db, get_collection, is_db_connected
from app.utils.auth_utils import hash_password
from app.data.career_domains_data import CAREER_DOMAINS
from app.data.gate_prep_data import GATE_QUESTIONS_CSE

fake = Faker()

BRANCHES = ['CSE', 'ECE', 'EEE', 'ME', 'Civil']
CAREER_GOALS = ['Job', 'Govt', 'Higher Studies']
INTERESTS_POOL = [
    'Machine Learning', 'Web Development', 'Mobile Apps', 'IoT', 
    'Data Science', 'Cybersecurity', 'Cloud Computing', 'AI',
    'Robotics', 'Blockchain', 'Game Development', 'DevOps'
]
TASK_TYPES = ['homework', 'assignment', 'mini-project', 'final-year-project']
SUBJECTS = ['Data Structures', 'Algorithms', 'Database Management', 'Operating Systems', 
            'Computer Networks', 'Machine Learning', 'Web Technologies', 'Software Engineering']


def safe_hash_password(password: str) -> str:
    """Safely hash password with 72-byte limit for bcrypt"""
    # Bcrypt has a maximum password length of 72 bytes
    # Truncate to ensure we're within the limit
    if isinstance(password, str):
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password = password_bytes[:72].decode('utf-8', errors='ignore')
    return hash_password(password)


def seed_career_domains():
    """Seed career domains data"""
    domains_collection = get_collection("career_domains")
    if domains_collection is None:
        print("[ERROR] Could not get career_domains collection")
        return []
        
    # Clear existing domains
    domains_collection.delete_many({})
    
    # Insert new domains
    domains_list = list(CAREER_DOMAINS.values())
    if domains_list:
        try:
            result = domains_collection.insert_many(domains_list)
            print(f"[OK] Created {len(result.inserted_ids)} career_domains")
            return result.inserted_ids
        except Exception as e:
            print(f"[ERROR] Failed to seed career domains: {e}")
            return []
    return []


def seed_students(count=30):
    """Create sample students"""
    users_collection = get_collection("users")
    
    # Create admin first
    try:
        admin = {
            "name": "Admin User",
            "email": "admin@aiconsular.com",
            "password": safe_hash_password("admin123"),
            "branch": "CSE",
            "year": 4,
            "interests": ["System Administration"],
            "career_goal": "Job",
            "role": "admin",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        users_collection.insert_one(admin)
        print(f"[OK] Created admin user: admin@aiconsular.com / admin123")
    except Exception as e:
        print(f"[ERROR] Failed to create admin user: {e}")
        raise
    
    # Create students
    students = []
    
    # Add demo student from documentation
    try:
        demo_student = {
            "name": "Demo Student",
            "email": "student.demo@university.edu",
            "password": safe_hash_password("demo123"),
            "branch": "CSE",
            "year": 3,
            "interests": ["Machine Learning", "Web Development", "AI"],
            "career_goal": "Job",
            "role": "student",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        students.append(demo_student)
    except Exception as e:
        print(f"[ERROR] Failed to create demo student: {e}")
        raise
    
    for i in range(count - 1):
        try:
            student = {
                "name": fake.name(),
                "email": f"student{i+1}@example.com",
                "password": safe_hash_password("password123"),
                "branch": random.choice(BRANCHES),
                "year": random.randint(1, 4),
                "interests": random.sample(INTERESTS_POOL, k=random.randint(2, 5)),
                "career_goal": random.choice(CAREER_GOALS),
                "role": "student",
                "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 365)),
                "updated_at": datetime.utcnow()
            }
            students.append(student)
        except Exception as e:
            print(f"[ERROR] Failed to create student {i+1}: {e}")
            # Continue with other students
            continue
    
    result = users_collection.insert_many(students)
    print(f"[OK] Created {len(result.inserted_ids)} student users")
    return result.inserted_ids


def seed_tasks(student_ids):
    """Create sample tasks for students"""
    tasks_collection = get_collection("tasks")
    
    tasks = []
    for student_id in student_ids:
        num_tasks = random.randint(3, 8)
        for _ in range(num_tasks):
            task = {
                "student_id": str(student_id),
                "type": random.choice(TASK_TYPES),
                "subject": random.choice(SUBJECTS),
                "title": fake.sentence(nb_words=6),
                "description": fake.paragraph(nb_sentences=3),
                "difficulty": random.choice(["easy", "medium", "hard"]),
                "status": random.choice(["pending", "in-progress", "completed"]),
                "ai_assistance_used": random.choice([True,False]),
                "conversation_history": [],
                "feedback": None,
                "completed_at": None,
                "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 90))
            }
            
            if task["status"] == "completed":
                task["completed_at"] = task["created_at"] + timedelta(days=random.randint(1, 14))
            
            tasks.append(task)
    
    result = tasks_collection.insert_many(tasks)
    print(f"[OK] Created {len(result.inserted_ids)} tasks")


def seed_activities(student_ids):
    """Create sample activities"""
    activities_collection = get_collection("activities")
    
    activities = []
    for student_id in student_ids:
        num_activities = random.randint(5, 15)
        for _ in range(num_activities):
            activity = {
                "student_id": str(student_id),
                "activity_type": random.choice(["task_completed", "skill_learned", "course_completed"]),
                "details": {},
                "skills_gained": random.sample(INTERESTS_POOL, k=random.randint(1, 3)),
                "weak_areas": [],
                "strong_areas": random.sample(SUBJECTS, k=random.randint(1, 3)),
                "timestamp": datetime.utcnow() - timedelta(days=random.randint(1, 180))
            }
            activities.append(activity)
    
    result = activities_collection.insert_many(activities)
    print(f"[OK] Created {len(result.inserted_ids)} activities")


def seed_courses():
    """Create sample course recommendations"""
    courses_collection = get_collection("courses")
    
    courses = [
        {
            "title": "Data Structures and Algorithms",
            "platform": "NPTEL",
            "domain": "Computer Science",
            "difficulty": "Intermediate",
            "duration": "12 weeks",
            "url": "https://nptel.ac.in/courses",
            "skills": ["Data Structures", "Algorithms", "Problem Solving"],
            "recommended_for": {"branches": ["CSE", "IT"], "career_paths": ["Software Engineering"]}
        },
        {
            "title": "Machine Learning Specialization",
            "platform": "Coursera",
            "domain": "Artificial Intelligence",
            "difficulty": "Advanced",
            "duration": "3 months",
            "url": "https://coursera.org",
            "skills": ["Machine Learning", "Python", "TensorFlow"],
            "recommended_for": {"branches": ["CSE", "ECE"], "career_paths": ["ML Engineer", "Data Scientist"]}
        },
        {
            "title": "Full Stack Web Development",
            "platform": "Udemy",
            "domain": "Web Development",
            "difficulty": "Beginner",
            "duration": "8 weeks",
            "url": "https://udemy.com",
            "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
            "recommended_for": {"branches": ["CSE", "IT"], "career_paths": ["Full Stack Developer"]}
        },
        {
            "title": "Introduction to Cybersecurity",
            "platform": "edX",
            "domain": "Security",
            "difficulty": "Beginner",
            "duration": "6 weeks",
            "url": "https://edx.org",
            "skills": ["Network Security", "Ethical Hacking", "Cryptography"],
            "recommended_for": {"branches": ["CSE", "IT"], "career_paths": ["Security Analyst"]}
        },
        {
            "title": "Digital Signal Processing",
            "platform": "NPTEL",
            "domain": "Electronics",
            "difficulty": "Advanced",
            "duration": "12 weeks",
            "url": "https://nptel.ac.in/courses",
            "skills": ["Signal Processing", "MATLAB"],
            "recommended_for": {"branches": ["ECE", "EEE"], "career_paths": ["Signal Processing Engineer"]}
        }
    ]
    
    result = courses_collection.insert_many(courses)
    print(f"[OK] Created {len(result.inserted_ids)} courses")


def seed_internships(student_ids):
    """Create sample internship applications"""
    internships_collection = get_collection("internships")
    
    companies = ['Google', 'Microsoft', 'Amazon', 'Meta', 'Netflix', 'TCS', 'Infosys', 'Wipro', 'StartupX', 'TechFlow']
    roles = ['Software Engineering Intern', 'Data Science Intern', 'Web Dev Intern', 'Frontend Intern', 'Backend Intern']
    domains = ['Software Engineering', 'Data Science', 'Web Development', 'Mobile Apps', 'Cybersecurity']
    statuses = ['applied', 'interviewing', 'offered', 'rejected']
    
    internships = []
    for student_id in student_ids:
        # Each student gets 1-3 applications
        num_apps = random.randint(1, 3)
        for _ in range(num_apps):
            internship = {
                "student_id": str(student_id),
                "company": random.choice(companies),
                "role": random.choice(roles),
                "domain": random.choice(domains),
                "status": random.choice(statuses),
                "notes": fake.sentence(),
                "ai_review": None,
                "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 60)),
                "updated_at": datetime.utcnow()
            }
            # Give some demo students a pre-existing review
            if random.random() > 0.7:
                internship["ai_review"] = f"Actionable Tip: Highlight your {random.choice(INTERESTS_POOL)} projects. This company values students with strong {random.choice(SUBJECTS)} fundamentals."
                
            internships.append(internship)
            
    result = internships_collection.insert_many(internships)
    print(f"[OK] Created {len(result.inserted_ids)} internship applications")


def seed_gate_questions():
    """Seed GATE practice questions"""
    questions_collection = get_collection("gate_questions")
    
    if questions_collection is None:
        print("[ERROR] Could not get gate_questions collection")
        return
        
    # Clear existing questions
    questions_collection.delete_many({})
    
    # Insert new questions
    if GATE_QUESTIONS_CSE:
        try:
            result = questions_collection.insert_many(GATE_QUESTIONS_CSE)
            print(f"[OK] Created {len(result.inserted_ids)} GATE questions")
        except Exception as e:
            print(f"[ERROR] Failed to seed GATE questions: {e}")


def main():
    """Run all seed functions"""
    print("[SEED] Starting database seeding...")
    
    connect_db()
    
    # Check if connection was successful
    if not is_db_connected():
        print("[ERROR] Could not connect to MongoDB.")
        print("Please ensure MongoDB is running and the connection URI is correct.")
        print("To start MongoDB locally on Windows, try running: net start MongoDB")
        sys.exit(1)
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("[WARN] Clearing existing data...")
    get_collection("users").delete_many({"role": {"$ne": "system"}})
    get_collection("tasks").delete_many({})
    get_collection("activities").delete_many({})
    get_collection("courses").delete_many({})
    get_collection("internships").delete_many({})
    
    # Seed data
    career_domain_ids = seed_career_domains()
    student_ids = seed_students(30)
    seed_tasks(student_ids)
    seed_activities(student_ids)
    seed_courses()
    seed_courses()
    seed_internships(student_ids)
    seed_gate_questions()
    
    print("\n[OK] Database seeding completed successfully!")
    print("\n[INFO] Demo Credentials:")
    print("   Admin: admin@aiconsular.com / admin123")
    print("   Student: student1@example.com / password123")
    print("   (Students 1-30 all use password123)")


if __name__ == "__main__":
    main()
