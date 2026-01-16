"""Application configuration with MongoDB and JWT settings."""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # MongoDB settings
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "ai_fashion_db"
    
    # JWT settings
    secret_key: str = "secret*key*for*jwt*token*generation"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS settings
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # GROQ API
    groq_api_key: str = "groq_api_key_value"
    
    # LLM Model
    llm_model: str = "llama-3.3-70b-versatile"
    
    # Case-insensitive property accessors
    @property
    def GROQ_API_KEY(self):
        return self.groq_api_key
    
    @property
    def LLM_MODEL(self):
        return self.llm_model
    
    @property
    def MONGODB_URL(self):
        return self.mongodb_url
    
    @property
    def MONGODB_DB_NAME(self):
        return self.mongodb_db_name
    
    @property
    def SECRET_KEY(self):
        return self.secret_key
    
    @property
    def ALGORITHM(self):
        return self.algorithm
    
    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self):
        return self.access_token_expire_minutes
    
    @property
    def REFRESH_TOKEN_EXPIRE_DAYS(self):
        return self.refresh_token_expire_days
    
    @property
    def ALLOWED_ORIGINS(self):
        return self.allowed_origins
    
    @property
    def ENVIRONMENT(self):
        return self.environment
    
    @property
    def DEBUG(self):
        return self.debug
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


settings = Settings()