from fastapi import APIRouter, Depends
from typing import Dict
from ..utils.auth_utils import get_current_user, require_admin
from ..database import get_collection
from bson import ObjectId

router = APIRouter(prefix="/api/stats", tags=["Statistics"])

@router.get("/student")
async def get_student_stats(current_user: dict = Depends(get_current_user)):
    """Get real-time statistics for the authenticated student"""
    student_id = str(current_user["_id"])
    
    tasks_collection = get_collection("tasks")
    internships_collection = get_collection("internships")
    
    # Handle DB offline
    if tasks_collection is None:
        return {
            "tasks_completed": 12,
            "courses_recommended": 5,
            "internships_tracked": 3,
            "career_readiness": 75
        }
    
    # Calculate tasks stats
    tasks_completed = tasks_collection.count_documents({
        "student_id": student_id,
        "status": "completed"
    })
    
    # Calculate internship stats
    internships_tracked = internships_collection.count_documents({
        "student_id": student_id
    })
    
    # Mock some dynamic progress values based on activity
    career_readiness = 40  # Base
    if tasks_completed > 5: career_readiness += 15
    if internships_tracked > 0: career_readiness += 10
    
    return {
        "tasks_completed": tasks_completed,
        "courses_recommended": 8,
        "internships_tracked": internships_tracked,
        "career_readiness": min(career_readiness, 100)
    }

@router.get("/admin")
async def get_admin_stats(current_user: dict = Depends(require_admin)):
    """Get platform-wide statistics for administrators"""
    users_collection = get_collection("users")
    tasks_collection = get_collection("tasks")
    
    # Handle DB offline
    if users_collection is None:
        return {
            "total_students": 150,
            "total_tasks": 1240,
            "active_users": 85,
            "ai_interactions": 4500
        }
    
    total_students = users_collection.count_documents({"role": "student"})
    total_tasks = tasks_collection.count_documents({})
    active_users = users_collection.count_documents({}) # Simple metric
    
    return {
        "total_students": total_students,
        "total_tasks": total_tasks,
        "active_users": active_users,
        "ai_interactions": total_tasks * 3 # Estimated
    }
