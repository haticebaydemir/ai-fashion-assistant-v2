"""Updated search endpoints with authentication and personalization."""

from fastapi import APIRouter, File, UploadFile, Form, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
from typing import Optional
from app.services.search_engine import FashionSearchEngine
from app.middleware.auth_middleware import get_optional_user
from app.models.auth_models import UserResponse
from app.database import get_profiles_collection, get_favorites_collection, get_history_collection
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Global search engine instance (lazy loaded)
_search_engine = None


def get_search_engine(request: Request = None) -> FashionSearchEngine:
    """Get or create search engine instance with ML loader."""
    global _search_engine
    if _search_engine is None:
        try:
            ml_loader = None
            if request and hasattr(request.app, 'state'):
                ml_loader = getattr(request.app.state, 'ml_loader', None)
            
            _search_engine = FashionSearchEngine(ml_loader)
            logger.info("✅ Search engine initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize search engine: {e}")
            raise RuntimeError(f"Search engine initialization failed: {e}")
    
    return _search_engine


async def apply_user_personalization(
    results: list,
    user_id: str,
    limit: int = 10
) -> list:
    """Apply personalization boosting to search results."""
    try:
        profiles_collection = get_profiles_collection()
        favorites_collection = get_favorites_collection()
        
        # Get user profile
        profile = await profiles_collection.find_one({"user_id": user_id})
        
        # Get favorites
        favorites_cursor = favorites_collection.find({"user_id": user_id})
        favorites = await favorites_cursor.to_list(length=100)
        favorite_ids = [f["product_id"] for f in favorites]
        
        # If no personalization data, return original results
        if not profile and not favorites:
            logger.info(f"No personalization data for user: {user_id}")
            return results[:limit]
        
        # Get user preferences
        user_colors = [c.lower() for c in profile.get("colors", [])] if profile else []
        user_styles = [s.lower() for s in profile.get("style", [])] if profile else []
        
        logger.info(f"✅ Personalizing for user {user_id}: colors={user_colors}, styles={user_styles}, favorites={len(favorite_ids)}")
        
        # Apply personalization boost
        for result in results:
            base_score = result.get("score", 0.5)
            boost = 0.0
            
            # Favorite boost (highest priority)
            if result.get("product_id") in favorite_ids:
                boost += 0.3
                logger.debug(f"Favorite boost: product_id={result.get('product_id')}")
            
            # Color boost
            result_color = result.get("color", "").lower()
            if result_color in user_colors:
                boost += 0.15
                logger.debug(f"Color boost: {result_color}")
            
            # Style/Category boost
            result_category = result.get("category", "").lower()
            if result_category in user_styles:
                boost += 0.1
                logger.debug(f"Category boost: {result_category}")
            
            # Calculate personalized score
            result["personalized_score"] = min(base_score + boost, 1.0)
            result["is_favorite"] = result.get("product_id") in favorite_ids
        
        # Sort by personalized score
        results = sorted(
            results, 
            key=lambda x: x.get("personalized_score", x.get("score", 0)), 
            reverse=True
        )
        
        logger.info(f"✅ Personalization applied: {len(results)} results re-ranked")
        return results[:limit]
        
    except Exception as e:
        logger.error(f"Personalization failed: {e}", exc_info=True)
        return results[:limit]


async def save_search_history(user_id: str, query: str, query_type: str, results_count: int):
    """Save search query to user's history."""
    try:
        history_collection = get_history_collection()
        await history_collection.insert_one({
            "user_id": user_id,
            "query": query,
            "query_type": query_type,
            "results_count": results_count,
            "timestamp": datetime.utcnow()
        })
        logger.debug(f"Search history saved: user={user_id}, type={query_type}")
    except Exception as e:
        logger.error(f"Failed to save search history: {e}")


@router.post("/text")
async def search_text(
    query: str = Form(...),
    k: int = Form(20),
    personalized: bool = Form(True),
    request: Request = None,
    current_user: Optional[UserResponse] = Depends(get_optional_user)
):
    """Text-based product search with optional personalization."""
    try:
        engine = get_search_engine(request)
        
        # Determine search parameters
        user_id = current_user.user_id if current_user else None
        is_personalized = personalized and user_id is not None
        
        # Search with expanded k if personalization is enabled
        search_k = k * 2 if is_personalized else k
        
        logger.info(f"Text search: query='{query}', k={search_k}, personalized={is_personalized}")
        
        # Perform search
        results = engine.search(text=query, k=search_k)
        results_list = [r.__dict__ for r in results]
        
        logger.info(f"Found {len(results_list)} results")
        
        # Apply personalization if enabled
        if is_personalized:
            results_list = await apply_user_personalization(
                results_list, 
                user_id, 
                limit=k
            )
        else:
            results_list = results_list[:k]
        
        # Save search history
        if user_id:
            await save_search_history(user_id, query, "text", len(results_list))
        
        return JSONResponse(content={
            "status": "success",
            "query": query,
            "results_count": len(results_list),
            "personalized": is_personalized,
            "results": results_list
        })
        
    except Exception as e:
        logger.error(f"Text search error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image")
async def search_image(
    image: UploadFile = File(...),
    k: int = Form(10),
    personalized: bool = Form(True),
    request: Request = None,
    current_user: Optional[UserResponse] = Depends(get_optional_user)
):
    """Image-based product search with optional personalization."""
    try:
        engine = get_search_engine(request)
        
        # Validate image
        contents = await image.read()
        if len(contents) == 0:
            raise ValueError("Empty image file")
        
        img = Image.open(io.BytesIO(contents)).convert('RGB')
        logger.info(f"Image loaded: {img.size}, mode: {img.mode}")
        
        # Search with expanded k if personalization is enabled
        search_k = k * 2 if (current_user and personalized) else k
        
        logger.info(f"Image search: k={search_k}, personalized={personalized and current_user is not None}")
        
        # Perform search
        try:
            results = engine.search(image=img, k=search_k)
        except Exception as search_error:
            logger.error(f"Search engine error: {search_error}", exc_info=True)
            raise RuntimeError(f"Search failed: {str(search_error)}")
        
        results_list = [r.__dict__ for r in results]
        logger.info(f"Found {len(results_list)} results")
        
        # Apply personalization if enabled
        if current_user and personalized:
            results_list = await apply_user_personalization(
                results_list, 
                current_user.user_id, 
                limit=k
            )
        else:
            results_list = results_list[:k]
        
        # Save search history
        if current_user:
            await save_search_history(
                current_user.user_id, 
                f"image:{image.filename}", 
                "image", 
                len(results_list)
            )
        
        return JSONResponse(content={
            "status": "success",
            "image_filename": image.filename,
            "results_count": len(results_list),
            "personalized": current_user is not None and personalized,
            "results": results_list
        })
        
    except Exception as e:
        logger.error(f"Image search error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/multimodal")
async def search_multimodal(
    query: str = Form(...),
    image: UploadFile = File(...),
    k: int = Form(10),
    alpha: float = Form(0.7),
    personalized: bool = Form(True),
    request: Request = None,
    current_user: Optional[UserResponse] = Depends(get_optional_user)
):
    """Multimodal product search (text + image) with optional personalization."""
    try:
        engine = get_search_engine(request)
        
        # Validate image
        contents = await image.read()
        if len(contents) == 0:
            raise ValueError("Empty image file")
            
        img = Image.open(io.BytesIO(contents)).convert('RGB')
        logger.info(f"Multimodal search: query='{query}', image={img.size}, alpha={alpha}")
        
        # Search with expanded k if personalization is enabled
        search_k = k * 2 if (current_user and personalized) else k
        
        logger.info(f"Multimodal search: k={search_k}, personalized={personalized and current_user is not None}")
        
        # Perform search
        try:
            results = engine.search(text=query, image=img, k=search_k, alpha=alpha)
        except Exception as search_error:
            logger.error(f"Search engine error: {search_error}", exc_info=True)
            raise RuntimeError(f"Search failed: {str(search_error)}")
        
        results_list = [r.__dict__ for r in results]
        logger.info(f"Found {len(results_list)} results")
        
        # Apply personalization if enabled
        if current_user and personalized:
            results_list = await apply_user_personalization(
                results_list, 
                current_user.user_id, 
                limit=k
            )
        else:
            results_list = results_list[:k]
        
        # Save search history
        if current_user:
            await save_search_history(
                current_user.user_id, 
                f"{query} + image:{image.filename}", 
                "multimodal", 
                len(results_list)
            )
        
        return JSONResponse(content={
            "status": "success",
            "query": query, 
            "image_filename": image.filename,
            "alpha": alpha,
            "results_count": len(results_list),
            "personalized": current_user is not None and personalized,
            "results": results_list
        })
        
    except Exception as e:
        logger.error(f"Multimodal search error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
