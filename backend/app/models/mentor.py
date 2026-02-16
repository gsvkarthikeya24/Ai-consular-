from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any

class MentorChatRequest(BaseModel):
    message: str = Field(..., examples=["How do I prepare for a data science interview?"])
    conversation_history: Optional[List[Dict[str, Any]]] = Field(default=[], examples=[[{"role": "user", "content": "Hi"}]])

class MentorChatResponse(BaseModel):
    response: str = Field(..., examples=["Focus on statistics, Python, and SQL."])
    timestamp: str = Field(..., examples=["2023-10-27T10:00:00Z"])

class MotivationResponse(BaseModel):
    message: str = Field(..., examples=["Keep pushing, you are doing great!"])
    timestamp: str = Field(..., examples=["2023-10-27T10:00:00Z"])

class ProductivityTip(BaseModel):
    title: str = Field(..., examples=["Pomodoro Technique"])
    description: str = Field(..., examples=["Work for 25 minutes, take a 5 minute break."])
    category: str = Field(..., examples=["Time Management"])
