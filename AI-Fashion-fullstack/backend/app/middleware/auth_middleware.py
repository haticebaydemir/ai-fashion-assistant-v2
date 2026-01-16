"""Authentication middleware and dependencies for protected routes."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.core.auth import verify_token, decode_token
from app.database import get_users_collection
from app.models.auth_models import UserResponse
import logging

logger = logging.getLogger(__name__)

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserResponse:
    """
    Dependency to get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials with JWT token
        
    Returns:
        UserResponse object with user data
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    # Verify token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user_id from token
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    try:
        users_collection = get_users_collection()
        user = await users_collection.find_one({"user_id": user_id})
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user account",
            )
        
        # Return user response (without sensitive data)
        return UserResponse(
            user_id=user["user_id"],
            name=user["name"],
            email=user["email"],
            created_at=user["created_at"],
            is_active=user.get("is_active", True)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Dependency to ensure user is active.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse if user is active
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[UserResponse]:
    """
    Dependency to get current user if authenticated, or None if not.
    Useful for endpoints that work both with and without authentication.
    
    Args:
        credentials: Optional HTTP Bearer credentials
        
    Returns:
        UserResponse if authenticated, None otherwise
    """
    if credentials is None:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user_id from JWT token without database lookup.
    
    Args:
        token: JWT token string
        
    Returns:
        user_id if valid token, None otherwise
    """
    return decode_token(token)


async def verify_user_access(
    user_id: str,
    current_user: UserResponse = Depends(get_current_user)
) -> bool:
    """
    Verify that current user has access to requested user's data.
    
    Args:
        user_id: User ID being accessed
        current_user: Current authenticated user
        
    Returns:
        True if access allowed
        
    Raises:
        HTTPException: If access denied
    """
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own data"
        )
    return True


class AuthenticationError(Exception):
    """Custom authentication error."""
    pass


class AuthorizationError(Exception):
    """Custom authorization error."""
    pass
