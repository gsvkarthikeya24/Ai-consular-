from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

class InternshipBase(BaseModel):
    company: str = Field(..., examples=["Google"])
    role: str = Field(..., examples=["Software Engineering Intern"])
    domain: str = Field(..., examples=["AI/ML"])
    status: str = Field(default="applied", examples=["applied"])
    notes: str = Field(default="", examples=["Referral from John"])

class InternshipCreate(InternshipBase):
    pass

class InternshipUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    domain: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class InternshipResponse(InternshipBase):
    id: str = Field(alias="_id", examples=["60f1b5b5b5b5b5b5b5b5b5b5"])
    student_id: str = Field(..., examples=["507f1f77bcf86cd799439011"])
    applied_date: Optional[datetime] = None
    ai_suggestions: List[Any] = Field(default=[], examples=[["Update resume with more keywords"]])
    updated_at: datetime
    ai_review: Optional[str] = Field(None, examples=["Your resume is a good match for this role."])

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "company": "Google",
                "role": "Software Engineering Intern",
                "domain": "AI/ML",
                "status": "applied",
                "notes": "Referral from John",
                "id": "60f1b5b5b5b5b5b5b5b5b5b5",
                "student_id": "507f1f77bcf86cd799439011",
                "applied_date": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00",
                "ai_suggestions": ["Update resume with more keywords"],
                "ai_review": "Your resume is a good match for this role."
            }
        }
    )

class InternshipReviewResponse(BaseModel):
    review: str = Field(..., examples=["Strong application, consider highlighting your Python skills."])
    internship_id: str = Field(..., examples=["60f1b5b5b5b5b5b5b5b5b5b5"])
