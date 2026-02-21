from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from ..data.quiz_data import QUIZ_QUESTIONS, BRANCH_DESCRIPTIONS
from ..utils.auth_utils import get_current_user

router = APIRouter(prefix="/api/quiz", tags=["Branch Selection Quiz"])

@router.get("/questions")
async def get_quiz_questions(current_user: dict = Depends(get_current_user)):
    """Fetch the 10 branch selection questions"""
    return QUIZ_QUESTIONS

from datetime import datetime, timezone
@router.post("/recommend")
async def get_branch_recommendation(
    answers: List[Dict[str, str]], 
    current_user: dict = Depends(get_current_user)
):
    """
    Analyze quiz answers and recommend an engineering branch.
    Input format: [{"question_id": 1, "option_id": "a"}, ...]
    """
    if len(answers) < 10:
        raise HTTPException(status_code=400, detail="Please answer all 10 questions.")

    # Tally points for each branch
    scores = {"CSE": 0, "ECE": 0, "EEE": 0, "ME": 0, "Civil": 0}
    
    question_map = {q["id"]: q for q in QUIZ_QUESTIONS}
    
    for ans in answers:
        q_id = int(ans["question_id"])
        opt_id = ans["option_id"]
        
        if q_id in question_map:
            question = question_map[q_id]
            option = next((o for o in question["options"] if o["id"] == opt_id), None)
            
            if option:
                points = option.get("points", {})
                for branch, val in points.items():
                    if branch in scores:
                        scores[branch] += val
                        
    # Determine recommended branch
    recommended_branch = max(scores, key=scores.get)
    
    return {
        "recommended_branch": recommended_branch,
        "description": BRANCH_DESCRIPTIONS.get(recommended_branch, "Engineering is a versatile field."),
        "scores": scores,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

