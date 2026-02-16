from fastapi import APIRouter, Depends
from typing import List, Dict
from ..database import get_collection
from ..utils.auth_utils import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/api/courses", tags=["Courses"])


@router.get("/recommendations")
async def get_course_recommendations(current_user: dict = Depends(get_current_user)):
    """Get personalized course recommendations for the student"""
    courses_collection = get_collection("courses")
    
    # Handle DB offline
    if courses_collection is None:
        return get_mock_courses()
    
    # Get user's branch and interests
    user_branch = current_user.get("branch", "CSE")
    user_interests = current_user.get("interests", [])
    
    # Find courses matching user's branch or interests
    try:
        all_courses = list(courses_collection.find({}))
        
        # If no courses in DB, return mock data
        if not all_courses:
            return get_mock_courses()
        
        # Score and sort courses based on relevance
        scored_courses = []
        for course in all_courses:
            score = 0
            
            # Check if branch matches
            if user_branch in course.get("recommended_for", {}).get("branches", []):
                score += 3
            
            # Check if interests match skills
            course_skills = course.get("skills", [])
            for interest in user_interests:
                if interest in course_skills:
                    score += 2
            
            # Convert ObjectId to string
            course["_id"] = str(course["_id"])
            course["relevance_score"] = score
            scored_courses.append(course)
        
        # Sort by relevance score
        scored_courses.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return scored_courses[:10]  # Return top 10
        
    except Exception as e:
        print(f"[ERROR] Failed to fetch courses: {e}")
        return get_mock_courses()


@router.get("/all")
async def get_all_courses(current_user: dict = Depends(get_current_user)):
    """Get all available courses"""
    courses_collection = get_collection("courses")
    
    # Handle DB offline
    if courses_collection is None:
        return get_mock_courses()
    
    try:
        courses = list(courses_collection.find({}))
        
        # If no courses, return mock data
        if not courses:
            return get_mock_courses()
        
        # Convert ObjectId to string
        for course in courses:
            course["_id"] = str(course["_id"])
        
        return courses
        
    except Exception:
        return get_mock_courses()


@router.get("/enrolled")
async def get_enrolled_courses(current_user: dict = Depends(get_current_user)):
    """Get details of courses the user is enrolled in"""
    courses_collection = get_collection("courses")
    
    # Handle DB offline
    if courses_collection is None:
        return []
    
    enrolled_ids = current_user.get("enrolled_courses", [])
    if not enrolled_ids:
        return []
        
    try:
        # Convert string IDs to ObjectIds where possible
        object_ids = []
        mock_ids = []
        for eid in enrolled_ids:
            if ObjectId.is_valid(eid):
                object_ids.append(ObjectId(eid))
            else:
                mock_ids.append(eid)
                
        # Fetch from DB
        courses = list(courses_collection.find({"_id": {"$in": object_ids}}))
        
        # Convert ObjectId to string
        for course in courses:
            course["_id"] = str(course["_id"])
            
        # Add mock courses if any (for testing mixed data)
        if mock_ids:
            mock_data = get_mock_courses()
            courses.extend([c for c in mock_data if c["_id"] in mock_ids])
            
        return courses
        
    except Exception as e:
        print(f"[ERROR] Failed to fetch enrolled courses: {e}")
        return []


@router.post("/{course_id}/enroll")
async def enroll_course(course_id: str, current_user: dict = Depends(get_current_user)):
    """Enroll a user in a course"""
    users_collection = get_collection("users")
    
    if users_collection is None:
        return {"message": "Database offline, cannot enroll", "success": False}
        
    try:
        # Handle both _id and id keys for compatibility
        user_id_str = current_user.get("_id") or current_user.get("id")
        user_id = ObjectId(user_id_str)
        
        # Add to set (avoid duplicates)
        result = users_collection.update_one(
            {"_id": user_id},
            {"$addToSet": {"enrolled_courses": course_id}}
        )
        
        if result.modified_count > 0:
            return {"message": "Successfully enrolled", "success": True, "course_id": course_id}
        else:
            return {"message": "Already enrolled or user not found", "success": True, "course_id": course_id}
            
    except Exception as e:
        print(f"[ERROR] Enrollment failed: {e}")
        return {"message": "Enrollment failed", "success": False}


def get_mock_courses() -> List[Dict]:
    """Return mock course data when database is offline"""
    return [
        {
            "_id": "mock-1",
            "title": "Data Structures and Algorithms",
            "platform": "NPTEL",
            "domain": "Computer Science",
            "difficulty": "Intermediate",
            "duration": "12 weeks",
            "url": "https://nptel.ac.in/courses",
            "skills": ["Data Structures", "Algorithms", "Problem Solving"],
            "recommended_for": {"branches": ["CSE", "IT"], "career_paths": ["Software Engineering"]},
            "relevance_score": 5
        },
        {
            "_id": "mock-2",
            "title": "Machine Learning Specialization",
            "platform": "Coursera",
            "domain": "Artificial Intelligence",
            "difficulty": "Advanced",
            "duration": "3 months",
            "url": "https://coursera.org",
            "skills": ["Machine Learning", "Python", "TensorFlow"],
            "recommended_for": {"branches": ["CSE", "ECE"], "career_paths": ["ML Engineer", "Data Scientist"]},
            "relevance_score": 4
        },
        {
            "_id": "mock-3",
            "title": "Full Stack Web Development",
            "platform": "Udemy",
            "domain": "Web Development",
            "difficulty": "Beginner",
            "duration": "8 weeks",
            "url": "https://udemy.com",
            "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
            "recommended_for": {"branches": ["CSE", "IT"], "career_paths": ["Full Stack Developer"]},
            "relevance_score": 3
        },
        {
            "_id": "mock-4",
            "title": "Cloud Computing Fundamentals",
            "platform": "AWS Training",
            "domain": "Cloud Computing",
            "difficulty": "Intermediate",
            "duration": "6 weeks",
            "url": "https://aws.amazon.com/training",
            "skills": ["AWS", "Cloud Architecture", "DevOps"],
            "recommended_for": {"branches": ["CSE", "IT"], "career_paths": ["Cloud Engineer", "DevOps Engineer"]},
            "relevance_score": 3
        },
        {
            "_id": "mock-5",
            "title": "Cybersecurity Essentials",
            "platform": "Cisco Networking Academy",
            "domain": "Cybersecurity",
            "difficulty": "Beginner",
            "duration": "10 weeks",
            "url": "https://www.netacad.com",
            "skills": ["Network Security", "Ethical Hacking", "Cryptography"],
            "recommended_for": {"branches": ["CSE", "ECE", "IT"], "career_paths": ["Security Analyst", "Ethical Hacker"]},
            "relevance_score": 2
        }
    ]
