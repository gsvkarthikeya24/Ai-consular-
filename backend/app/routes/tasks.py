from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from bson import ObjectId
from typing import List
from ..models.task import (
    TaskCreate, 
    TaskResponse, 
    TaskAssistanceRequest, 
    TaskAssistanceResponse,
    ConversationMessage
)
from ..database import get_collection
from ..utils.auth_utils import get_current_user
from ..services.ai_service import ai_service

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new task"""
    tasks_collection = get_collection("tasks")
    
    task_dict = task_data.model_dump()
    task_dict.update({
        "student_id": str(current_user["_id"]),
        "status": "pending",
        "ai_assistance_used": False,
        "conversation_history": [],
        "feedback": None,
        "completed_at": None,
        "created_at": datetime.utcnow()
    })
    
    result = tasks_collection.insert_one(task_dict)
    task_dict["_id"] = str(result.inserted_id)
    
    return TaskResponse(
        id=task_dict["_id"],
        type=task_dict["type"],
        subject=task_dict["subject"],
        title=task_dict["title"],
        description=task_dict["description"],
        difficulty=task_dict["difficulty"],
        status=task_dict["status"],
        ai_assistance_used=task_dict["ai_assistance_used"],
        created_at=task_dict["created_at"]
    )


@router.get("", response_model=List[TaskResponse])
async def get_tasks(current_user: dict = Depends(get_current_user)):
    """Get all tasks for current student"""
    tasks_collection = get_collection("tasks")
    
    tasks = list(tasks_collection.find({"student_id": str(current_user["_id"])}).sort("created_at", -1))
    
    return [
        TaskResponse(
            id=str(task["_id"]),
            type=task["type"],
            subject=task["subject"],
            title=task["title"],
            description=task["description"],
            difficulty=task.get("difficulty", "medium"),
            status=task["status"],
            ai_assistance_used=task.get("ai_assistance_used", False),
            created_at=task["created_at"]
        )
        for task in tasks
    ]


@router.get("/{task_id}")
async def get_task(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get specific task"""
    tasks_collection = get_collection("tasks")
    
    try:
        task = tasks_collection.find_one({"_id": ObjectId(task_id), "student_id": str(current_user["_id"])})
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task["_id"] = str(task["_id"])
    return task


@router.post("/{task_id}/assist", response_model=TaskAssistanceResponse)
async def get_task_assistance(
    task_id: str,
    request: TaskAssistanceRequest,
    current_user: dict = Depends(get_current_user)
):
    """Get AI assistance for a task"""
    tasks_collection = get_collection("tasks")
    
    try:
        task = tasks_collection.find_one({"_id": ObjectId(task_id), "student_id": str(current_user["_id"])})
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Get student's activity history for context
    activities_collection = get_collection("activities")
    activities = list(activities_collection.find({"student_id": str(current_user["_id"])}).limit(10))
    
    student_history = {
        "weak_areas": [],
        "strong_areas": []
    }
    for activity in activities:
        student_history["weak_areas"].extend(activity.get("weak_areas", []))
        student_history["strong_areas"].extend(activity.get("strong_areas", []))

    
    # Get AI response
    ai_response = await ai_service.academic_assistance(
        task_description=f"{task['title']}: {task['description']}\n\nStudent question: {request.message}",
        branch=current_user["branch"],
        task_type=task["type"],
        student_history=student_history if student_history["weak_areas"] or student_history["strong_areas"] else None
    )
    
    # Update conversation history
    conversation_history = task.get("conversation_history", [])
    conversation_history.append({
        "role": "user",
        "content": request.message,
        "timestamp": datetime.utcnow()
    })
    conversation_history.append({
        "role": "assistant",
        "content": ai_response,
        "timestamp": datetime.utcnow()
    })
    
    # Update task
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {
            "$set": {
                "conversation_history": conversation_history,
                "ai_assistance_used": True,
                "status": "in-progress" if task["status"] == "pending" else task["status"]
            }
        }
    )
    
    return TaskAssistanceResponse(
        response=ai_response,
        conversation_history=[
            ConversationMessage(**msg) for msg in conversation_history
        ]
    )


@router.put("/{task_id}/complete")
async def complete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Mark task as completed"""
    tasks_collection = get_collection("tasks")
    activities_collection = get_collection("activities")
    
    try:
        task = tasks_collection.find_one({"_id": ObjectId(task_id), "student_id": str(current_user["_id"])})
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update task status
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {
            "$set": {
                "status": "completed",
                "completed_at": datetime.utcnow()
            }
        }
    )
    
    # Log activity
    activities_collection.insert_one({
        "student_id": str(current_user["_id"]),
        "activity_type": "task_completed",
        "details": {
            "task_id": task_id,
            "task_type": task["type"],
            "subject": task["subject"],
            "title": task["title"]
        },
        "skills_gained": [],  # Can be enhanced with NLP
        "weak_areas": [],
        "strong_areas": [],
        "timestamp": datetime.utcnow()
    })
    
    return {"message": "Task marked as completed"}


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a task"""
    tasks_collection = get_collection("tasks")
    
    try:
        result = tasks_collection.delete_one({"_id": ObjectId(task_id), "student_id": str(current_user["_id"])})
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully"}
