# AI Consular - Intelligent Academic & Career Guidance System

A comprehensive full-stack AI-powered platform for B-Tech students providing academic assistance, career guidance, resume building, and mentorship.

## 🚀 Features

- **Authentication & Profile Management** - Secure JWT-based auth with student profiles
- **Academic Task Assistance** - AI-powered help for homework, assignments, and projects
- **Career Recommendations** - Personalized career path suggestions based on student profile
- **Resume Builder** - AI-generated content with ATS score optimization
- **AI Mentor** - 24/7 academic and motivational support
- **Progress Tracking** - Comprehensive dashboards with analytics
- **Internship Tracker** - Manage job/internship applications
- **GATE Preparation** - Track syllabus, practice questions, and study plans
- **Admin Analytics** - Platform insights and reporting
- **Task Management** - Create, track, and complete academic tasks with AI assistance

## 🛠️ Tech Stack

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- React Router
- Axios
- Chart.js
- Lucide Icons

**Backend:**
- Python 3.11+
- FastAPI
- MongoDB
- OpenAI API / Google Gemini
- JWT Authentication
- Pydantic

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB (local or MongoDB Atlas)
- Google Gemini API key

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd puri
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Copy .env.example to .env and add your API keys:
# - GEMINI_API_KEY=your-key-here
# - MONGODB_URI=your-mongodb-connection-string
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### 4. Database Setup

Make sure MongoDB is running. If you don't have MongoDB installed, the application will automatically fall back to an **In-Memory Demo Mode**.

**Seed demo data (if not using demo mode):**
```bash
cd backend
python -m app.seed_data
```

This creates:
- 30 sample students
- Sample tasks, activities, and courses
- Admin account: `admin@aiconsular.com` / `admin123`
- Student accounts: `student1@example.com` / `password123`

## 🚀 Running the Application

### Option 1: Using Batch Scripts (Windows)

```bash
# Start backend
start_backend.bat

# Start frontend (in another terminal)
start_frontend.bat
```

### Option 2: Manual Start

**Backend:**
```bash
cd backend
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### Access the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## 👤 Demo Accounts

**Admin:**
- Email: `admin@aiconsular.com`
- Password: `admin123`

**Students:**
- Email: `student1@example.com` (or student2, student3, etc.)
- Password: `password123`

## 📁 Project Structure

```
puri/
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── models/          # Pydantic models
│   │   ├── services/        # Business logic & AI integration
│   │   ├── utils/           # Helper functions
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # MongoDB connection
│   │   ├── main.py          # FastAPI app
│   │   └── seed_data.py     # Demo data generator
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── utils/           # Helper functions
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── package.json
│   └── .env
├── render.yaml              # Render Deployment Blueprint
├── start_backend.bat
├── start_frontend.bat
└── README.md
```

## 🔑 Environment Variables

**Backend (`.env`):**
```
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=ai_consular
JWT_SECRET=your-secret-key
GEMINI_API_KEY=your-gemini-key
```

**Frontend (`.env`):**
```
VITE_API_URL=http://localhost:8000
```

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new student
- `POST /api/auth/login` - Login
- `GET /api/auth/profile` - Get profile

### Tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks/{id}/assist` - Get AI assistance

### Quiz & Recommendations
- `POST /api/quiz/submit` - Submit branch selection quiz
- `POST /api/career/recommend` - Get recommendations

### Mentor
- `POST /api/mentor/chat` - Chat with AI mentor

## 🚢 Deployment (Render)

This project is configured for automated deployment on **Render** using a Blueprint (`render.yaml`).

### Deployment Steps
1. **Push to GitHub**: Push your latest changes to your repository.
2. **Open Render**: Go to [dashboard.render.com](https://dashboard.render.com).
3. **New Blueprint**: Click **New +** -> **Blueprint**.
4. **Select Repository**: Connect and select your project repository.
5. **Configure Environment**: Provide the following variables when prompted:
   - `MONGODB_URI`: Your database connection string (e.g., MongoDB Atlas or Neon PostgreSQL).
   - `GEMINI_API_KEY`: Your Google Gemini API key.
6. **Deploy**: Click **Apply** and Render will automatically provision:
   - **Backend**: A Python web service running FastAPI.
   - **Frontend**: A highly optimized **Static Site** with built-in CDN support.

> [!NOTE]
> The Blueprint automatically handles the linking between frontend and backend, so you don't need to manually configure the `FRONTEND_URL` or `VITE_API_URL`.

---

**Built with ❤️ for B-Tech Students**
