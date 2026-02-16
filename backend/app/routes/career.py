from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List, Dict
from ..utils.auth_utils import get_current_user
from ..services.ai_service import ai_service
from ..data import (
    get_all_domains,
    get_domain_by_id,
    get_domains_by_category,
    search_domains,
    CAREER_CATEGORIES
)

from ..models.career import (
    CareerDomainListResponse, 
    CareerCategoryResponse, 
    CareerDomain, 
    CareerRecommendationResponse, 
    DetailedRecommendationResponse, 
    SkillGapResponse, 
    RoadmapResponse, 
    RequirementsResponse
)

router = APIRouter(prefix="/api/career", tags=["Career"])


@router.get("/domains", response_model=CareerDomainListResponse)
async def get_career_domains(
    category: Optional[str] = Query(None, description="Filter by category"),
    keyword: Optional[str] = Query(None, description="Search by keyword"),
    required_skill: Optional[str] = Query(None, description="Filter by required skill")
):
    """
    Get all career domains with optional filtering
    
    - **category**: Filter by category (e.g., "Software & AI", "Cybersecurity & Banking")
    - **keyword**: Search domains by keyword in title/description
    - **required_skill**: Filter domains requiring a specific skill
    """
    
    # Get domains based on filters
    if category:
        domains = get_domains_by_category(category)
    elif keyword:
        domains = search_domains(keyword)
    else:
        domains = get_all_domains()
    
    # Additional filtering by required skill
    if required_skill and domains:
        skill_lower = required_skill.lower()
        domains = [
            d for d in domains
            if any(skill_lower in skill['name'].lower() for skill in d['key_skills'])
        ]
    
    return {
        "total_count": len(domains),
        "domains": domains
    }


@router.get("/categories", response_model=CareerCategoryResponse)
async def get_career_categories():
    """Get all career categories with domain counts"""
    category_info = []
    for category, domain_ids in CAREER_CATEGORIES.items():
        category_info.append({
            "category": category,
            "count": len(domain_ids),
            "domain_ids": domain_ids
        })
    
    return {
        "categories": category_info
    }


@router.get("/domains/{domain_id}", response_model=CareerDomain)
async def get_domain_detail(domain_id: str):
    """Get detailed information about a specific career domain"""
    domain = get_domain_by_id(domain_id)
    
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    return domain


@router.post("/recommend", response_model=CareerRecommendationResponse)
async def get_career_recommendations(current_user: dict = Depends(get_current_user)):
    """
    Generate AI-powered career recommendations for student
    Analyzes student profile, interests, branch, and completed tasks
    """
    
    # Get student's activity data for skills analysis
    # This would typically query the activities collection
    skills_analysis = {
        "skills": []  # Extracted from completed tasks
    }
    
    result = await ai_service.career_recommendation(
        branch=current_user["branch"],
        interests=current_user.get("interests", []),
        career_goal=current_user.get("career_goal", "Job"),
        skills_analysis=skills_analysis if skills_analysis["skills"] else None
    )
    
    return {
        "recommendations": result,
        "student_profile": {
            "branch": current_user["branch"],
            "interests": current_user.get("interests", []),
            "career_goal": current_user.get("career_goal")
        }
    }


@router.post("/recommend/detailed", response_model=DetailedRecommendationResponse)
async def get_detailed_recommendations(current_user: dict = Depends(get_current_user)):
    """
    Get detailed AI career recommendations with domain matching scores
    Returns top 5 matching domains with reasoning and skill gap analysis
    """
    
    branch = current_user.get("branch", "Computer Science")
    interests = current_user.get("interests", [])
    completed_tasks_count = current_user.get("completed_tasks", 0)
    cgpa = current_user.get("cgpa", 7.5)
    
    # Build context for AI matching
    student_context = f"""
Student Profile:
- Branch: {branch}
- Interests: {', '.join(interests) if interests else 'Not specified'}
- Completed Tasks: {completed_tasks_count}
- CGPA: {cgpa}
"""

    result = await ai_service.detailed_career_matching(
        student_context=student_context,
        available_domains=get_all_domains()
    )
    
    return {
        "recommended_domains": result,
        "student_profile": {
            "branch": branch,
            "interests": interests,
            "cgpa": cgpa
        }
    }


@router.post("/skill-gap", response_model=SkillGapResponse)
async def analyze_skill_gap(
    target_domain_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Analyze skill gap between student's current skills and target domain requirements
    """
    domain = get_domain_by_id(target_domain_id)
    
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    # Get student's current skills (from profile or inferred from tasks)
    student_skills = current_user.get("skills", [])
    
    # Required skills from domain
    required_skills = domain['key_skills']
    
    # Calculate gap
    student_skill_names = {s.lower() if isinstance(s, str) else s.get('name', '').lower() 
                          for s in student_skills}
    
    skills_have = []
    skills_need = []
    
    for req_skill in required_skills:
        skill_name = req_skill['name'].lower()
        matched = False
        for student_skill in student_skill_names:
            if skill_name in student_skill or student_skill in skill_name:
                skills_have.append(req_skill)
                matched = True
                break
        if not matched:
            skills_need.append(req_skill)
    
    gap_percentage = (len(skills_need) / len(required_skills) * 100) if required_skills else 0
    readiness_score = 100 - gap_percentage
    
    return {
        "domain": domain['title'],
        "domain_id": target_domain_id,
        "readiness_score": round(readiness_score, 1),
        "skills_you_have": skills_have,
        "skills_you_need": skills_need,
        "total_required": len(required_skills),
        "skills_matched": len(skills_have),
        "skills_missing": len(skills_need),
        "roadmap": domain['roadmap_phases']
    }


@router.get("/roadmap/{domain_id}", response_model=RoadmapResponse)
async def get_domain_roadmap(domain_id: str):
    """Get personalized learning roadmap for a specific domain"""
    domain = get_domain_by_id(domain_id)
    
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    return {
        "domain": domain['title'],
        "domain_id": domain_id,
        "roadmap_phases": domain['roadmap_phases'],
        "certifications": domain['certifications'],
        "key_skills": domain['key_skills'],
        "estimated_duration": sum(
            int(phase.get('duration', '0 months').split()[0]) 
            for phase in domain['roadmap_phases']
        )
    }


@router.get("/requirements/{domain_id}", response_model=RequirementsResponse)
async def get_entry_requirements(domain_id: str):
    """Get entry requirements for a specific domain (especially useful for DRDO, ISRO)"""
    domain = get_domain_by_id(domain_id)
    
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    return {
        "domain": domain['title'],
        "domain_id": domain_id,
        "entry_requirements": domain.get('entry_requirements', {}),
        "required_education": domain.get('required_education', []),
        "certifications": domain.get('certifications', []),
        "salary_range": domain.get('salary_range', {}),
        "top_companies": domain.get('top_companies', []),
        "job_market_outlook": domain.get('job_market_outlook', 'Not specified')
    }


@router.get("/paths", response_model=Dict[str, List[str]])
async def get_career_paths():
    """Get available career paths grouped by category (legacy endpoint)"""
    return CAREER_CATEGORIES

