"""Authentication API endpoints: register, login, logout, token refresh."""

from fastapi import APIRouter, HTTPException, status, Depends
from app.models.auth_models import (
    UserRegister, UserLogin, TokenResponse, TokenRefresh,
    UserResponse, PasswordChange, ErrorResponse
)
from app.core.auth import (
    get_password_hash, verify_password, create_token_pair,
    verify_token, create_access_token
)
from app.database import get_users_collection, get_profiles_collection
from app.middleware.auth_middleware import get_current_user
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user account.
    
    - **name**: Full name (2-100 characters)
    - **email**: Valid email address (unique)
    - **password**: Strong password (min 8 chars, must contain uppercase, lowercase, digit)
    
    Returns JWT access token and refresh token.
    """
    try:
        users_collection = get_users_collection()
        
        # Check if email already exists
        existing_user = await users_collection.find_one({"email": user_data.email.lower()})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Generate unique user_id
        user_id = f"usr_{uuid.uuid4().hex[:16]}"
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user document
        user_doc = {
            "user_id": user_id,
            "name": user_data.name,
            "email": user_data.email.lower(),
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "last_login": None,
            "is_active": True,
            "is_verified": False,
            "style": [],
            "size": None,
            "colors": [],
            "total_searches": 0,
            "total_favorites": 0
        }
        
        # Insert user into database
        await users_collection.insert_one(user_doc)
        
        # Create initial profile
        profiles_collection = get_profiles_collection()
        profile_doc = {
            "user_id": user_id,
            "style": [],
            "size": None,
            "colors": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        await profiles_collection.insert_one(profile_doc)
        
        # Generate tokens
        tokens = create_token_pair(user_id, user_data.email.lower())
        
        logger.info(f"✅ New user registered: {user_data.email}")
        
        return TokenResponse(**tokens)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    Authenticate user and return JWT tokens.
    
    - **email**: User's registered email
    - **password**: User's password
    
    Returns access token and refresh token.
    """
    try:
        users_collection = get_users_collection()
        
        # Find user by email
        user = await users_collection.find_one({"email": credentials.email.lower()})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify password
        if not verify_password(credentials.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user is active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive. Please contact support."
            )
        
        # Update last login time
        await users_collection.update_one(
            {"user_id": user["user_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        # Generate tokens
        tokens = create_token_pair(user["user_id"], user["email"])
        
        logger.info(f"✅ User logged in: {user['email']}")
        
        return TokenResponse(**tokens)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again."
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: TokenRefresh):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    
    Returns new access token and refresh token.
    """
    try:
        # Verify refresh token
        payload = verify_token(token_data.refresh_token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check token type
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        email = payload.get("email")
        
        if not user_id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Verify user still exists and is active
        users_collection = get_users_collection()
        user = await users_collection.find_one({"user_id": user_id})
        
        if not user or not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account not found or inactive"
            )
        
        # Generate new token pair
        tokens = create_token_pair(user_id, email)
        
        logger.info(f"✅ Token refreshed for user: {email}")
        
        return TokenResponse(**tokens)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user: UserResponse = Depends(get_current_user)):
    """
    Logout current user (client should delete tokens).
    
    Note: JWT tokens are stateless, so server-side logout just logs the event.
    Client must delete tokens from storage.
    """
    logger.info(f"✅ User logged out: {current_user.email}")
    
    return {
        "message": "Successfully logged out",
        "user_id": current_user.user_id
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    
    Returns user profile without sensitive data.
    """
    return current_user


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: PasswordChange,
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Change user's password.
    
    - **old_password**: Current password
    - **new_password**: New password (must be strong)
    """
    try:
        users_collection = get_users_collection()
        
        # Get user with password
        user = await users_collection.find_one({"user_id": current_user.user_id})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify old password
        if not verify_password(password_data.old_password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid current password"
            )
        
        # Hash new password
        new_hashed_password = get_password_hash(password_data.new_password)
        
        # Update password
        await users_collection.update_one(
            {"user_id": current_user.user_id},
            {"$set": {"hashed_password": new_hashed_password}}
        )
        
        logger.info(f"✅ Password changed for user: {current_user.email}")
        
        return {
            "message": "Password successfully changed",
            "user_id": current_user.user_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Password change error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed"
        )


@router.delete("/account", status_code=status.HTTP_200_OK)
async def delete_account(current_user: UserResponse = Depends(get_current_user)):
    """
    Delete user account (soft delete - sets is_active to False).
    
    Warning: This action cannot be undone.
    """
    try:
        users_collection = get_users_collection()
        
        # Soft delete: set is_active to False
        await users_collection.update_one(
            {"user_id": current_user.user_id},
            {"$set": {"is_active": False, "deleted_at": datetime.utcnow()}}
        )
        
        logger.info(f"✅ Account deleted for user: {current_user.email}")
        
        return {
            "message": "Account successfully deleted",
            "user_id": current_user.user_id
        }
        
    except Exception as e:
        logger.error(f"❌ Account deletion error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Account deletion failed"
        )
