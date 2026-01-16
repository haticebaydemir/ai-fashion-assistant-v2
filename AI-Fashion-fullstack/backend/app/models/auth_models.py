"""Pydantic models for authentication and user management."""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import re


class UserRegister(BaseModel):
    """User registration request model."""
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=100, description="Password (min 8 characters)")
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        """Validate name format."""
        if not v.strip():
            raise ValueError('Name cannot be empty')
        if not re.match(r'^[a-zA-ZğüşıöçĞÜŞİÖÇ\s\-]+$', v):
            raise ValueError('Name can only contain letters, spaces, and hyphens')
        return v.strip()


class UserLogin(BaseModel):
    """User login request model."""
    email: EmailStr = Field(..., description="User's email")
    password: str = Field(..., min_length=8, description="User's password")


class TokenResponse(BaseModel):
    """Token response model."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes in seconds


class TokenRefresh(BaseModel):
    """Token refresh request model."""
    refresh_token: str


class UserResponse(BaseModel):
    """User response model (without sensitive data)."""
    user_id: str
    name: str
    email: str
    created_at: datetime
    is_active: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "usr_1234567890",
                "name": "Hatice Baydemir",
                "email": "hatice@example.com",
                "created_at": "2026-01-13T10:00:00",
                "is_active": True
            }
        }


class UserProfileUpdate(BaseModel):
    """User profile update model."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    style: Optional[List[str]] = Field(None, description="Style preferences")
    size: Optional[str] = Field(None, description="Clothing size")
    colors: Optional[List[str]] = Field(None, description="Favorite colors")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Hatice Baydemir",
                "style": ["casual", "elegant", "modern"],
                "size": "M",
                "colors": ["black", "navy", "white"]
            }
        }


class PasswordChange(BaseModel):
    """Password change request model."""
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_new_password(cls, v, values):
        """Validate new password."""
        if 'old_password' in values and v == values['old_password']:
            raise ValueError('New password must be different from old password')
        
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserInDB(BaseModel):
    """User model as stored in database."""
    user_id: str
    name: str
    email: str
    hashed_password: str
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    is_verified: bool = False
    
    # Profile data
    style: Optional[List[str]] = []
    size: Optional[str] = None
    colors: Optional[List[str]] = []
    
    # Stats
    total_searches: int = 0
    total_favorites: int = 0


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str
    error_code: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid credentials",
                "error_code": "AUTH_001"
            }
        }
