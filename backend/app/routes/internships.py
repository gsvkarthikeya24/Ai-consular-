from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime, timezone
from bson import ObjectId
from ..utils.auth_utils import get_current_user
from ..database import get_collection
from ..services.ai_service import ai_service
from ..models.internship import InternshipCreate, InternshipUpdate, InternshipResponse, InternshipReviewResponse

router = APIRouter(prefix="/api/internships", tags=["Internships"])


@router.post("", response_model=InternshipResponse)
async def add_internship(
    internship_data: InternshipCreate,
    current_user: dict = Depends(get_current_user)
):
    """Add new internship application"""
    internships_collection = get_collection("internships")
    
    internship_dict = internship_data.model_dump()
    internship_dict.update({
        "student_id": str(current_user["_id"]),
        "applied_date": datetime.now(timezone.utc),
        "ai_suggestions": [],
        "updated_at": datetime.now(timezone.utc)
    })
    
    result = internships_collection.insert_one(internship_dict)
    internship_dict["_id"] = str(result.inserted_id)
    
    return internship_dict


@router.get("", response_model=List[InternshipResponse])
async def get_internships(current_user: dict = Depends(get_current_user)):
    """Get all internship applications"""
    internships_collection = get_collection("internships")
    
    internships = list(internships_collection.find({"student_id": str(current_user["_id"])}).sort("applied_date", -1))
    
    for internship in internships:
        internship["_id"] = str(internship["_id"])
    
    return internships


@router.put("/{internship_id}")
async def update_internship(
    internship_id: str,
    update_data: InternshipUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update internship status"""
    internships_collection = get_collection("internships")
    
    update_dict = update_data.model_dump(exclude_unset=True)
    update_dict["updated_at"] = datetime.now(timezone.utc)
    
    result = internships_collection.update_one(
        {"_id": ObjectId(internship_id), "student_id": str(current_user["_id"])},
        {"$set": update_dict}
    )
    
    if result.matched_count == 0:
        return {"error": "Internship not found"}
    
    return {"message": "Internship updated successfully"}


@router.delete("/{internship_id}")
async def delete_internship(
    internship_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete internship application"""
    internships_collection = get_collection("internships")
    
    result = internships_collection.delete_one(
        {"_id": ObjectId(internship_id), "student_id": str(current_user["_id"])}
    )
    
    if result.deleted_count == 0:
        return {"error": "Internship not found"}
    
    return {"message": "Internship deleted successfully"}


@router.post("/{internship_id}/review", response_model=InternshipReviewResponse)
async def get_internship_ai_review(
    internship_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get AI review for a specific internship application"""
    internships_collection = get_collection("internships")
    
    internship = internships_collection.find_one({
        "_id": ObjectId(internship_id),
        "student_id": str(current_user["_id"])
    })
    
    if not internship:
        return {"error": "Internship not found"}
    
    # Get review from AI service
    review_data = await ai_service.internship_review(
        internship_data=internship,
        student_profile=current_user
    )
    
    # Optionally store the review in the database
    internships_collection.update_one(
        {"_id": ObjectId(internship_id)},
        {"$set": {"ai_review": review_data["review"], "updated_at": datetime.now(timezone.utc)}}
    )
    
    return {
        "review": review_data["review"],
        "internship_id": internship_id
    }
