from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "ai_consular"
    
    # JWT
    jwt_secret: str = "demo-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # LLM Configuration
    llm_provider: str = "gemini"  # only gemini supported now
    gemini_api_key: Optional[str] = None

    
    # Environment
    environment: str = "development"
    frontend_url: str = "http://localhost:5173"
    allowed_hosts: str = "*"
    
    class Config:
        # Look for .env in the backend directory
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        case_sensitive = False


settings = Settings()
