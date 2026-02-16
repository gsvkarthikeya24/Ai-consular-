from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any
from datetime import datetime

class SkillRequirement(BaseModel):
    name: str = Field(..., examples=["Python"])
    level: str = Field(..., examples=["Intermediate"])

class RoadmapPhase(BaseModel):
    phase: str = Field(..., examples=["Phase 1: Basics"])
    duration: str = Field(..., examples=["2 months"])
    focus: str = Field(..., examples=["Syntax, Data Structures"])

class EntryRequirements(BaseModel):
    degree: Optional[str] = Field(None, examples=["B.Tech in CS"])
    gate_required: bool = Field(False, examples=[True])
    certifications_mandatory: Any = Field(False, examples=[False])  # Can be bool or str based on data
    age_limit: Optional[str] = Field(None, examples=["28 years"])
    nationality: Optional[str] = Field(None, examples=["Indian"])
    gate_subject: Optional[str] = Field(None, examples=["CS/IT"])

class SalaryRange(BaseModel):
    fresher: Optional[str] = Field(None, examples=["4-6 LPA"])
    mid_level: Optional[str] = Field(None, examples=["10-15 LPA"])
    senior: Optional[str] = Field(None, examples=["25+ LPA"])
    scientist_b: Optional[str] = Field(None, examples=["Level 10"])
    scientist_c: Optional[str] = Field(None, examples=["Level 11"])

class CareerDomain(BaseModel):
    domain_id: str = Field(..., examples=["software-engineering"])
    title: str = Field(..., examples=["Software Engineering"])
    category: str = Field(..., examples=["IT"])
    description: str = Field(..., examples=["Developing software applications."])
    required_education: List[str] = Field(..., examples=[["B.Tech CS", "MCA"]])
    key_skills: List[SkillRequirement] = Field(..., examples=[[{"name": "Python", "level": "High"}]])
    certifications: List[str] = Field(default=[], examples=[["AWS Certified"]])
    roadmap_phases: List[RoadmapPhase] = Field(..., examples=[[{"phase": "1", "duration": "1 month", "focus": "Basics"}]])
    entry_requirements: Optional[EntryRequirements] = None
    salary_range: Optional[SalaryRange] = None
    top_companies: Optional[List[str]] = Field(None, examples=[["Google", "Microsoft"]])
    top_organizations: Optional[List[str]] = Field(None, examples=[["ISRO", "DRDO"]])  # For DRDO etc
    job_market_outlook: Optional[str] = Field(None, examples=["High demand"])
    keywords_for_ats: Optional[List[str]] = Field(None, examples=[["Software", "Development"]])

class CareerDomainListResponse(BaseModel):
    total_count: int = Field(..., examples=[10])
    domains: List[CareerDomain]

class CareerCategoryInfo(BaseModel):
    category: str = Field(..., examples=["IT"])
    count: int = Field(..., examples=[5])
    domain_ids: List[str] = Field(..., examples=[["software-engineering"]])

class CareerCategoryResponse(BaseModel):
    categories: List[CareerCategoryInfo]

class StudentProfile(BaseModel):
    branch: Optional[str] = Field(None, examples=["CS"])
    interests: Optional[List[str]] = Field(None, examples=[["Coding"]])
    career_goal: Optional[str] = Field(None, examples=["Developer"])
    cgpa: Optional[float] = Field(None, examples=[8.5])

class CareerRecommendationResponse(BaseModel):
    recommendations: Any = Field(..., examples=[{"paths": []}])  # The AI response dict
    student_profile: StudentProfile

class DetailedRecommendationResponse(BaseModel):
    recommended_domains: Any = Field(..., examples=[{"matches": []}]) # The AI response dict
    student_profile: StudentProfile

class SkillGapResponse(BaseModel):
    domain: str = Field(..., examples=["Software Engineering"])
    domain_id: str = Field(..., examples=["software-engineering"])
    readiness_score: float = Field(..., examples=[75.5])
    skills_you_have: List[SkillRequirement] = Field(..., examples=[[{"name": "Python", "level": "Intermediate"}]])
    skills_you_need: List[SkillRequirement] = Field(..., examples=[[{"name": "Docker", "level": "Basic"}]])
    total_required: int = Field(..., examples=[10])
    skills_matched: int = Field(..., examples=[5])
    skills_missing: int = Field(..., examples=[5])
    roadmap: List[RoadmapPhase] = Field(..., examples=[[{"phase": "1", "duration": "1 month", "focus": "Docker"}]])

class RoadmapResponse(BaseModel):
    domain: str = Field(..., examples=["Software Engineering"])
    domain_id: str = Field(..., examples=["software-engineering"])
    roadmap_phases: List[RoadmapPhase]
    certifications: List[str] = Field(..., examples=[["AWS"]])
    key_skills: List[SkillRequirement]
    estimated_duration: int = Field(..., examples=[6]) # months

class RequirementsResponse(BaseModel):
    domain: str = Field(..., examples=["Software Engineering"])
    domain_id: str = Field(..., examples=["software-engineering"])
    entry_requirements: Optional[EntryRequirements] = None
    required_education: List[str] = Field(..., examples=[["B.Tech"]])
    certifications: List[str] = Field(..., examples=[["AWS"]])
    salary_range: Optional[SalaryRange] = None
    top_companies: Optional[List[str]] = Field(None, examples=[["Google"]])
    job_market_outlook: Optional[str] = Field(None, examples=["Growing"])
