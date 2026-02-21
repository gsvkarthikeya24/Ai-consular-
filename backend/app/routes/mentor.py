from fastapi import APIRouter, Depends
from typing import List
from datetime import datetime, timezone
from ..utils.auth_utils import get_current_user
from ..services.ai_service import ai_service
from ..models.mentor import MentorChatRequest, MentorChatResponse, MotivationResponse, ProductivityTip

router = APIRouter(prefix="/api/mentor", tags=["AI Mentor"])



@router.post("/chat", response_model=MentorChatResponse)
async def chat_with_mentor(
    request: MentorChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """Chat with AI mentor"""
    
    response = await ai_service.mentor_chat(
        user_message=request.message,
        conversation_history=request.conversation_history
    )
    
    return {
        "response": response,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/motivation", response_model=MotivationResponse)
async def get_motivation(current_user: dict = Depends(get_current_user)):
    """Get motivational message"""
    
    message = await ai_service.generate_motivation()
    
    return {
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/tips", response_model=List[ProductivityTip])
async def get_productivity_tips():
    """Get productivity tips"""
    tips = [
        {
            "title": "Pomodoro Technique",
            "description": "Work for 25 minutes, then take a 5-minute break. Repeat 4 times, then take a longer break.",
            "category": "Time Management"
        },
        {
            "title": "Active Recall",
            "description": "Test yourself on what you've learned instead of passively re-reading notes.",
            "category": "Study Technique"
        },
        {
            "title": "Spaced Repetition",
            "description": "Review material at increasing intervals to strengthen long-term memory.",
            "category": "Study Technique"
        },
        {
            "title": "Time Blocking",
            "description": "Dedicate specific time blocks to different subjects or tasks throughout your day.",
            "category": "Time Management"
        }
    ]
    
    return tips
