from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from typing import List, Optional, Dict
from ..utils.auth_utils import get_current_user
from ..utils.file_utils import extract_text_from_pdf
from ..services.ai_service import ai_service
from ..database import get_collection
from bson import ObjectId
from datetime import datetime
from ..models.resume import (
    ResumeData,
    ResumeResponse,
    ATSCheckRequest,
    ATSAnalysisResponse,
    ResumeBase
)

router = APIRouter(prefix="/api/resume", tags=["Resume"])


@router.post("/generate")
async def generate_resume_content(
    resume_data: ResumeData,
    current_user: dict = Depends(get_current_user)
):
    """Generate AI-powered resume content"""
    
    projects_list = [p.model_dump() for p in resume_data.projects]
    
    result = await ai_service.resume_content_generation(
        projects=projects_list,
        skills=resume_data.skills,
        branch=current_user["branch"],
        target_domain=resume_data.target_domain
    )
    
    return result


@router.post("/ats-check", response_model=ATSAnalysisResponse)
async def check_ats_score(
    request: ATSCheckRequest,
    current_user: dict = Depends(get_current_user)
):
    """Check ATS score for resume"""
    
    result = await ai_service.ats_analysis(
        resume_text=request.resume_text,
        job_description=request.job_description
    )
    
    return result


@router.post("/ats-check-upload")
async def check_ats_score_upload(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """Check ATS score for uploaded resume file (PDF)"""
    
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    contents = await file.read()
    resume_text = extract_text_from_pdf(contents)
    
    if not resume_text:
        raise HTTPException(status_code=400, detail="Could not extract text from the PDF file")
    
    result = await ai_service.ats_analysis(
        resume_text=resume_text,
        job_description=job_description
    )
    
    return result


@router.get("/templates")
async def get_resume_templates():
    """Get available resume templates"""
    templates = [
        {
            "id": "modern",
            "name": "Modern Professional",
            "description": "Clean and modern design suitable for tech roles"
        },
        {
            "id": "classic",
            "name": "Classic ATS",
            "description": "Traditional format optimized for ATS"
        },
        {
            "id": "creative",
            "name": "Creative Designer",
            "description": "Visually appealing for creative roles"
        }
    ]
    
    return templates


@router.post("")
async def save_resume(
    resume_data: ResumeBase,
    current_user: dict = Depends(get_current_user)
):
    """Save or update resume"""
    resumes_collection = get_collection("resumes")
    
    data_dict = resume_data.model_dump(exclude_unset=True)
    data_dict["student_id"] = str(current_user["_id"])
    data_dict["updated_at"] = datetime.utcnow()
    
    # Check if resume exists
    existing = resumes_collection.find_one({"student_id": str(current_user["_id"])})
    
    if existing:
        resumes_collection.update_one(
            {"student_id": str(current_user["_id"])},
            {"$set": data_dict}
        )
        return {"message": "Resume updated successfully"}
    else:
        data_dict["created_at"] = datetime.utcnow()
        resumes_collection.insert_one(data_dict)
        return {"message": "Resume created successfully"}


@router.get("", response_model=ResumeResponse)
async def get_resume(current_user: dict = Depends(get_current_user)):
    """Get student's resume"""
    resumes_collection = get_collection("resumes")
    
    resume = resumes_collection.find_one({"student_id": str(current_user["_id"])})
    
    if not resume:
        # Return empty structure or 404? 
        # Usually 404 if meaningful data is expected, but empty resume might be valid state
        # Let's return 404 for consistency
        return {"message": "No resume found"}
    
    resume["_id"] = str(resume["_id"])
    return resume
