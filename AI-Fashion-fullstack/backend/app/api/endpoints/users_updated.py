"""Updated user management endpoints with authentication."""

from fastapi import APIRouter, Request, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
from datetime import datetime
import logging

from app.middleware.auth_middleware import get_current_user, verify_user_access
from app.models.auth_models import UserResponse
from app.database import (
    get_profiles_collection,
    get_favorites_collection,
    get_history_collection
)

logger = logging.getLogger(__name__)

router = APIRouter()


# ==================== PROFILE ENDPOINTS ====================

@router.get("/{user_id}/profile")
async def get_profile(
    user_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user profile (must be authenticated as the user)."""
    await verify_user_access(user_id, current_user)  # ✅ await added
    
    try:
        profiles_collection = get_profiles_collection()
        profile = await profiles_collection.find_one({"user_id": user_id})
        
        if not profile:
            return JSONResponse(content={
                "profile": {
                    "user_id": user_id,
                    "style": [],
                    "size": "",
                    "colors": [],
                    "budget": ""
                }
            })
        
        # ✅ Remove datetime fields
        profile.pop("_id", None)
        profile.pop("created_at", None)
        profile.pop("updated_at", None)
        
        # Ensure correct types
        if not isinstance(profile.get("style"), list):
            profile["style"] = []
        if not isinstance(profile.get("colors"), list):
            profile["colors"] = []
        if not isinstance(profile.get("size"), str):
            profile["size"] = ""
        if not isinstance(profile.get("budget"), str):
            profile["budget"] = ""
        
        return JSONResponse(content={"profile": profile})
        
    except Exception as e:
        logger.error(f"Get profile error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{user_id}/profile")
async def update_profile(
    user_id: str,
    profile: dict,
    current_user: UserResponse = Depends(get_current_user)
):
    """Update user profile preferences."""
    await verify_user_access(user_id, current_user)  # ✅ await added
    
    try:
        profiles_collection = get_profiles_collection()
        
        # Build profile data with correct types
        profile_data = {
            "user_id": user_id,
            "style": profile.get("style", []) if isinstance(profile.get("style"), list) else [],
            "colors": profile.get("colors", []) if isinstance(profile.get("colors"), list) else [],
            "size": str(profile.get("size", "")) if profile.get("size") else "",
            "budget": str(profile.get("budget", "")) if profile.get("budget") else "",
            "updated_at": datetime.utcnow()
        }
        
        # Update or insert profile
        await profiles_collection.update_one(
            {"user_id": user_id},
            {"$set": profile_data},
            upsert=True
        )
        
        logger.info(f"✅ Profile updated for user: {user_id}")
        
        # Return updated profile (without datetime)
        updated_profile = await profiles_collection.find_one({"user_id": user_id})
        if updated_profile:
            updated_profile.pop("_id", None)
            updated_profile.pop("created_at", None)
            updated_profile.pop("updated_at", None)  # ✅ Remove datetime
        
        return JSONResponse(content={
            "message": "Profile updated successfully",
            "profile": updated_profile
        })
        
    except Exception as e:
        logger.error(f"Update profile error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==================== FAVORITES ENDPOINTS ====================

@router.get("/{user_id}/favorites")
async def get_favorites(
    user_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user's favorite products."""
    await verify_user_access(user_id, current_user)  # ✅ await added
    
    try:
        favorites_collection = get_favorites_collection()
        
        cursor = favorites_collection.find({"user_id": user_id}).sort("added_at", -1)
        favorites = await cursor.to_list(length=1000)
        
        # Remove MongoDB fields
        for fav in favorites:
            fav.pop("_id", None)
            fav.pop("added_at", None)  # ✅ Remove datetime
        
        return JSONResponse(content={
            "favorites": favorites,
            "total": len(favorites)
        })
        
    except Exception as e:
        logger.error(f"Get favorites error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/{user_id}/favorites")
async def add_favorite(
    user_id: str,
    favorite: dict,
    current_user: UserResponse = Depends(get_current_user)
):
    """Add product to favorites."""
    await verify_user_access(user_id, current_user)  # ✅ await added
    
    try:
        favorites_collection = get_favorites_collection()
        
        existing = await favorites_collection.find_one({
            "user_id": user_id,
            "product_id": favorite["product_id"]
        })
        
        if existing:
            existing.pop("_id", None)
            existing.pop("added_at", None)  # ✅ Remove datetime
            return JSONResponse(content={
                "message": "Already in favorites",
                "favorite": existing
            })
        
        favorite_doc = {
            "user_id": user_id,
            "product_id": favorite["product_id"],
            "product_name": favorite.get("product_name", ""),
            "category": favorite.get("category", ""),
            "color": favorite.get("color", ""),
            "image_url": favorite.get("image_url"),
            "added_at": datetime.utcnow()
        }
        
        result = await favorites_collection.insert_one(favorite_doc)
        favorite_doc.pop("_id", None)
        favorite_doc.pop("added_at", None)  # ✅ Remove datetime
        
        logger.info(f"✅ Favorite added: user={user_id}, product={favorite['product_id']}")
        
        return JSONResponse(content={
            "message": "Added to favorites",
            "favorite": favorite_doc
        })
        
    except Exception as e:
        logger.error(f"Add favorite error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{user_id}/favorites/{product_id}")
async def remove_favorite(
    user_id: str,
    product_id: int,
    current_user: UserResponse = Depends(get_current_user)
):
    """Remove product from user's favorites."""
    await verify_user_access(user_id, current_user)  # ✅ await added
    
    try:
        favorites_collection = get_favorites_collection()
        
        result = await favorites_collection.delete_one({
            "user_id": user_id,
            "product_id": product_id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found"
            )
        
        logger.info(f"✅ Product {product_id} removed from favorites for user {user_id}")
        
        return JSONResponse(content={
            "status": "removed",
            "product_id": product_id
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Remove favorite error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==================== SEARCH HISTORY ENDPOINTS ====================

@router.get("/{user_id}/history")
async def get_search_history(
    user_id: str,
    limit: int = 50,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user's search history."""
    await verify_user_access(user_id, current_user)  # ✅ await added
    
    try:
        history_collection = get_history_collection()
        
        cursor = history_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
        history = await cursor.to_list(length=limit)
        
        # Convert datetime to string
        for entry in history:
            entry.pop("_id", None)
            if "timestamp" in entry:
                entry["timestamp"] = entry["timestamp"].isoformat()  # ✅ Convert to string
        
        return JSONResponse(content={
            "history": history,
            "total": len(history)
        })
        
    except Exception as e:
        logger.error(f"Get history error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{user_id}/history")
async def clear_search_history(
    user_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Clear user's search history."""
    await verify_user_access(user_id, current_user)  # ✅ await added
    
    try:
        history_collection = get_history_collection()
        
        result = await history_collection.delete_many({"user_id": user_id})
        
        logger.info(f"✅ History cleared for user {user_id}: {result.deleted_count} entries")
        
        return JSONResponse(content={
            "status": "cleared",
            "deleted_count": result.deleted_count
        })
        
    except Exception as e:
        logger.error(f"Clear history error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ==================== STATS ENDPOINTS ====================

@router.get("/{user_id}/stats")
async def get_user_stats(
    user_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get user statistics."""
    await verify_user_access(user_id, current_user)  # ✅ await added
    
    try:
        profiles_collection = get_profiles_collection()
        favorites_collection = get_favorites_collection()
        history_collection = get_history_collection()
        
        profile = await profiles_collection.find_one({"user_id": user_id})
        favorites_count = await favorites_collection.count_documents({"user_id": user_id})
        history_count = await history_collection.count_documents({"user_id": user_id})
        
        return JSONResponse(content={
            "user_id": user_id,
            "name": current_user.name,
            "email": current_user.email,
            "favorites_count": favorites_count,
            "history_count": history_count,
            "created_at": current_user.created_at.isoformat() if hasattr(current_user.created_at, 'isoformat') else str(current_user.created_at),  # ✅ Convert
            "profile": {
                "style": profile.get("style", []) if profile else [],
                "size": profile.get("size", "") if profile else "",
                "colors": profile.get("colors", []) if profile else [],
                "budget": profile.get("budget", "") if profile else ""
            }
        })
        
    except Exception as e:
        logger.error(f"Get stats error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
