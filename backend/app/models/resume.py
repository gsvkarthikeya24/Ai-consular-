from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Dict
from datetime import datetime

class ResumeProject(BaseModel):
    title: str = Field(..., examples=["E-commerce Website"])
    description: str = Field(..., examples=["Built a full-stack e-commerce site using React and Node.js"])
    technologies: List[str] = Field(default=[], examples=[["React", "Node.js", "MongoDB"]])

class ResumeData(BaseModel):
    projects: List[ResumeProject] = Field(default=[])
    skills: List[str] = Field(default=[], examples=[["Python", "JavaScript"]])
    target_domain: Optional[str] = Field(default="Software Engineering", examples=["Software Engineering"])

class ResumeBase(BaseModel):
    student_id: str = Field(..., examples=["507f1f77bcf86cd799439011"])
    personal_info: Optional[Dict[str, Any]] = Field(None, examples=[{"name": "John Doe", "email": "john@example.com"}])
    education: Optional[List[Dict[str, Any]]] = Field(None, examples=[[{"degree": "B.Tech", "institution": "IIT Bombay"}]])
    experience: Optional[List[Dict[str, Any]]] = Field(None, examples=[[{"role": "Intern", "company": "Google"}]])
    projects: Optional[List[ResumeProject]] = None
    skills: Optional[List[str]] = Field(None, examples=[["Python", "Java"]])
    certifications: Optional[List[str]] = Field(None, examples=[["AWS Certified Developer"]])
    achievements: Optional[List[str]] = Field(None, examples=[["Won Hackathon 2023"]])

class ResumeResponse(ResumeBase):
    id: str = Field(alias="_id", examples=["60f1b5b5b5b5b5b5b5b5b5b5"])
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "student_id": "507f1f77bcf86cd799439011",
                "skills": ["Python", "Java"],
                "target_domain": "Software Engineering",
                "id": "60f1b5b5b5b5b5b5b5b5b5b5",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
    )

class ATSCheckRequest(BaseModel):
    resume_text: str = Field(..., examples=["Experienced software engineer with..."])
    job_description: Optional[str] = Field(None, examples=["We are looking for a software engineer..."])

class ATSAnalysisResponse(BaseModel):
    ats_score: int = Field(..., examples=[85])
    keywords_found: List[str] = Field(default=[], examples=[["Python", "FastAPI"]])
    keywords_missing: List[str] = Field(..., examples=[["Kubernetes", "Docker"]])
    suggestions: List[str] = Field(..., examples=[["Add more quantifiable achievements"]])
    match_details: Optional[Dict[str, Any]] = None
