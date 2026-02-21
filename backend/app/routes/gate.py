from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime, timezone
from ..database import get_collection
from ..utils.auth_utils import get_current_user
from ..data.gate_prep_data import (
    GATE_SUBJECTS,
    GATE_QUESTIONS_CSE,
    GATE_RESOURCES,
    GATE_YEAR_ANALYSIS
)

router = APIRouter(prefix="/api/gate", tags=["GATE Preparation"])


# Request/Response Models
class AnswerSubmission(BaseModel):
    question_id: str
    selected_answer: int
    time_taken: int  # in seconds


class QuestionResponse(BaseModel):
    question_id: str
    correct: bool
    explanation: str
    marks_awarded: int


@router.get("/subjects")
async def get_gate_subjects(current_user: dict = Depends(get_current_user)):
    """Get GATE subjects for user's branch"""
    user_branch = current_user.get("branch", "CSE")
    
    subjects = GATE_SUBJECTS.get(user_branch, GATE_SUBJECTS["CSE"])
    
    return {
        "branch": user_branch,
        "subjects": subjects,
        "total_subjects": len(subjects)
    }


@router.get("/questions")
async def get_gate_questions(
    subject: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get GATE practice questions"""
    questions_collection = get_collection("gate_questions")
    
    # Use mock data if DB offline or empty
    if questions_collection is None:
        return get_mock_questions(subject, difficulty, limit)
    
    try:
        # Build query
        query = {}
        if subject:
            query["subject"] = subject
        if difficulty:
            query["difficulty"] = difficulty
        
        questions = list(questions_collection.find(query).limit(limit))
        
        # If no questions in DB, return mock data
        if not questions:
            return get_mock_questions(subject, difficulty, limit)
        
        # Remove correct answer from response (for practice mode)
        for q in questions:
            q["_id"] = str(q["_id"])
            q["question_id"] = q["_id"]
            # Don't send correct_answer to client
            q.pop("correct_answer", None)
        
        return questions
        
    except Exception as e:
        print(f"[ERROR] Failed to fetch GATE questions: {e}")
        return get_mock_questions(subject, difficulty, limit)


@router.post("/submit-answer")
async def submit_answer(
    submission: AnswerSubmission,
    current_user: dict = Depends(get_current_user)
):
    """Submit answer and get feedback"""
    questions_collection = get_collection("gate_questions")
    progress_collection = get_collection("gate_progress")
    
    # Find the question (from DB or mock data)
    question = None
    if questions_collection:
        try:
            from bson import ObjectId
            question = questions_collection.find_one({"_id": ObjectId(submission.question_id)})
        except:
            pass
    
    # If not found in DB, search mock data
    if not question:
        for i, q in enumerate(GATE_QUESTIONS_CSE):
            if str(q.get("_id", "")) == submission.question_id or \
               str(i) == submission.question_id:
                question = q
                break

    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check answer
    correct_answer = question.get("correct_answer", 0)
    is_correct = submission.selected_answer == correct_answer
    marks = question.get("marks", 2) if is_correct else 0
    
    # Save progress
    if progress_collection:
        try:
            progress_entry = {
                "user_id": current_user.get("id"),
                "question_id": submission.question_id,
                "subject": question.get("subject"),
                "topic": question.get("topic"),
                "difficulty": question.get("difficulty"),
                "selected_answer": submission.selected_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "marks_awarded": marks,
                "time_taken": submission.time_taken,
                "timestamp": datetime.now(timezone.utc)
            }
            progress_collection.insert_one(progress_entry)
        except Exception as e:
            print(f"[ERROR] Failed to save progress: {e}")
    
    return {
        "question_id": submission.question_id,
        "correct": is_correct,
        "correct_answer": correct_answer,
        "explanation": question.get("explanation", ""),
        "marks_awarded": marks,
        "total_marks": question.get("marks", 2)
    }


@router.get("/progress")
async def get_gate_progress(current_user: dict = Depends(get_current_user)):
    """Get user's GATE preparation progress"""
    progress_collection = get_collection("gate_progress")
    
    if not progress_collection:
        return get_mock_progress()
    
    try:
        user_id = current_user.get("id")
        progress_data = list(progress_collection.find({"user_id": user_id}))
        
        if not progress_data:
            return get_mock_progress()
        
        # Calculate statistics
        total_attempted = len(progress_data)
        total_correct = sum(1 for p in progress_data if p.get("is_correct"))
        total_marks = sum(p.get("marks_awarded", 0) for p in progress_data)
        accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0
        
        # Subject-wise breakdown
        subject_stats = {}
        for entry in progress_data:
            subject = entry.get("subject", "Unknown")
            if subject not in subject_stats:
                subject_stats[subject] = {"attempted": 0, "correct": 0, "marks": 0}
            
            subject_stats[subject]["attempted"] += 1
            if entry.get("is_correct"):
                subject_stats[subject]["correct"] += 1
            subject_stats[subject]["marks"] += entry.get("marks_awarded", 0)
        
        # Calculate accuracy for each subject
        for subject in subject_stats:
            attempted = subject_stats[subject]["attempted"]
            correct = subject_stats[subject]["correct"]
            subject_stats[subject]["accuracy"] = (correct / attempted * 100) if attempted > 0 else 0
        
        return {
            "total_attempted": total_attempted,
            "total_correct": total_correct,
            "total_marks": total_marks,
            "accuracy": round(accuracy, 2),
            "subject_wise": subject_stats
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to fetch progress: {e}")
        return get_mock_progress()


@router.get("/resources")
async def get_gate_resources(
    subject: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get GATE study resources"""
    if subject:
        resources = [r for r in GATE_RESOURCES if r["subject"] == subject]
        return resources
    
    return GATE_RESOURCES


@router.get("/analysis")
async def get_year_analysis(
    year: Optional[int] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get previous year GATE analysis"""
    if year:
        return GATE_YEAR_ANALYSIS.get(str(year), {})
    
    return GATE_YEAR_ANALYSIS


# Helper functions
def get_mock_questions(subject: Optional[str], difficulty: Optional[str], limit: int):
    """Return mock GATE questions"""
    questions = GATE_QUESTIONS_CSE.copy()
    
    # Filter by subject
    if subject:
        questions = [q for q in questions if q.get("subject") == subject]
    
    # Filter by difficulty
    if difficulty:
        questions = [q for q in questions if q.get("difficulty") == difficulty]
    
    # Limit results
    questions = questions[:limit]
    
    # Add question_id and remove correct_answer
    for i, q in enumerate(questions):
        q["question_id"] = str(i)
        q_copy = q.copy()
        q_copy.pop("correct_answer", None)
        questions[i] = q_copy
    
    return questions


def get_mock_progress():
    """Return mock progress data"""
    return {
        "total_attempted": 15,
        "total_correct": 11,
        "total_marks": 22,
        "accuracy": 73.33,
        "subject_wise": {
            "Data Structures": {
                "attempted": 5,
                "correct": 4,
                "marks": 8,
                "accuracy": 80.0
            },
            "Algorithms": {
                "attempted": 4,
                "correct": 3,
                "marks": 6,
                "accuracy": 75.0
            },
            "Operating Systems": {
                "attempted": 3,
                "correct": 2,
                "marks": 4,
                "accuracy": 66.67
            },
            "Database Management Systems": {
                "attempted": 3,
                "correct": 2,
                "marks": 4,
                "accuracy": 66.67
            }
        }
    }
