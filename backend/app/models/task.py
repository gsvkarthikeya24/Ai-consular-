from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TaskBase(BaseModel):
    """Base task model"""
    type: str  # homework, assignment, mini-project, final-year-project
    subject: str
    title: str
    description: str
    difficulty: Optional[str] = "medium"  # easy, medium, hard


class TaskCreate(TaskBase):
    """Task creation model"""
    pass


class ConversationMessage(BaseModel):
    """Conversation message model"""
    role: str  # user or assistant
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TaskInDB(TaskBase):
    """Task in database model"""
    id: str = Field(alias="_id")
    student_id: str
    status: str = "pending"  # pending, in-progress, completed
    ai_assistance_used: bool = False
    conversation_history: List[ConversationMessage] = []
    feedback: Optional[str] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        populate_by_name = True


class TaskResponse(TaskBase):
    """Task response model"""
    id: str
    status: str
    ai_assistance_used: bool
    created_at: datetime
    
    class Config:
        populate_by_name = True


class TaskAssistanceRequest(BaseModel):
    """Request for AI assistance on a task"""
    message: str


class TaskAssistanceResponse(BaseModel):
    """AI assistance response"""
    response: str
    conversation_history: List[ConversationMessage]
