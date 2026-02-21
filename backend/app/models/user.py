from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """Base user model"""
    name: str = Field(..., examples=["John Doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    branch: str = Field(..., examples=["Computer Science"])
    year: int = Field(..., ge=1, le=4, examples=[3])
    interests: List[str] = Field(default=[], examples=[["AI", "Web Development"]])
    career_goal: str = Field(..., examples=["Job"])  # "Job" | "Govt" | "Higher Studies"
    enrolled_courses: List[str] = Field(default=[], examples=[["course_id_1", "course_id_2"]])


class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., examples=["securepassword123"])


class UserUpdate(BaseModel):
    """User update model"""
    name: Optional[str] = Field(None, examples=["John Doe"])
    branch: Optional[str] = Field(None, examples=["Computer Science"])
    year: Optional[int] = Field(None, ge=1, le=4, examples=[3])
    interests: Optional[List[str]] = Field(None, examples=[["AI", "Web Development"]])
    career_goal: Optional[str] = Field(None, examples=["Higher Studies"])


class UserInDB(UserBase):
    """User in database model"""
    id: str = Field(alias="_id", examples=["507f1f77bcf86cd799439011"])
    role: str = Field(default="student", examples=["student"])
    login_count: int = Field(default=0, examples=[5])
    last_login: Optional[datetime] = Field(default=None)
    status: str = Field(default="inactive", examples=["active"])
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "branch": "Computer Science",
                "year": 3,
                "interests": ["AI", "Web Development"],
                "career_goal": "Job",
                "id": "507f1f77bcf86cd799439011",
                "role": "student",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
    )


class UserResponse(UserBase):
    """User response model"""
    id: str = Field(..., examples=["507f1f77bcf86cd799439011"])
    role: str = Field(..., examples=["student"])
    login_count: int = Field(default=0)
    last_login: Optional[datetime] = Field(default=None)
    status: str = Field(default="inactive")
    created_at: datetime
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "branch": "Computer Science",
                "year": 3,
                "interests": ["AI", "Web Development"],
                "career_goal": "Job",
                "id": "507f1f77bcf86cd799439011",
                "role": "student",
                "created_at": "2023-01-01T00:00:00"
            }
        }
    )


class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., examples=["password123"])


class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
