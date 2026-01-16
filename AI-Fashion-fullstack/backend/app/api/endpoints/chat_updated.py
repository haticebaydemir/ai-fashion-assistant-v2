"""Updated chat endpoints with user authentication and personalization."""

from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.services.chat_service import ChatService
from app.services.search_engine import FashionSearchEngine
from app.services.rag_service import FashionRAGPipeline
from app.core.agent import FashionAgent
from app.core.memory import ConversationMemory
from app.core.personalization import PersonalizationEngine
from app.middleware.auth_middleware import get_current_user, get_optional_user
from app.models.auth_models import UserResponse
from app.database import get_favorites_collection, get_history_collection, get_profiles_collection
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
chat_service = ChatService()
rag_pipeline = FashionRAGPipeline()

# Global agent and memory (per-session management)
_agents = {}
_memories = {}
_personalization_engine = None


def get_personalization_engine():
    """Get or initialize personalization engine."""
    global _personalization_engine
    if _personalization_engine is None:
        try:
            products_df = pd.read_csv("data/meta_ssot.csv")
            _personalization_engine = PersonalizationEngine(products_df)
        except Exception as e:
            logger.error(f"Failed to initialize personalization engine: {e}")
    return _personalization_engine


class ChatRequest(BaseModel):
    """Chat request with user authentication support."""
    session_id: str
    message: str
    include_search: bool = True
    use_personalization: bool = True  # ✅ NEW


class RAGRequest(BaseModel):
    """RAG request with personalization."""
    query: str
    top_k: int = 5
    use_cache: bool = True
    use_personalization: bool = True  # ✅ NEW


async def personalize_search_results(
    results: List,
    user_id: str,
    limit: int = 10
) -> List:
    """
    Apply personalization to search results based on user preferences and favorites.
    
    Args:
        results: Raw search results
        user_id: User ID for personalization
        limit: Number of results to return
        
    Returns:
        Personalized and reranked results
    """
    try:
        # Get user data
        profiles_collection = get_profiles_collection()
        favorites_collection = get_favorites_collection()
        
        profile = await profiles_collection.find_one({"user_id": user_id})
        favorites_cursor = favorites_collection.find({"user_id": user_id})
        favorites = await favorites_cursor.to_list(length=100)
        
        if not profile and not favorites:
            return results[:limit]
        
        # Get personalization engine
        engine = get_personalization_engine()
        if not engine:
            return results[:limit]
        
        # Extract user preferences
        user_prefs = {
            "colors": profile.get("colors", []) if profile else [],
            "style": profile.get("style", []) if profile else [],
            "categories": []
        }
        
        # Get favorite product IDs
        favorite_ids = [f["product_id"] for f in favorites]
        
        # Score boost for matching preferences
        scored_results = []
        for result in results:
            score = result.get("score", 0.5)
            
            # Boost if in favorites
            if result.get("product_id") in favorite_ids:
                score += 0.3
            
            # Boost if color matches preferences
            if user_prefs["colors"] and result.get("color") in user_prefs["colors"]:
                score += 0.1
            
            # Boost if category matches history (simplified)
            if result.get("category") in user_prefs.get("categories", []):
                score += 0.05
            
            result["personalized_score"] = min(score, 1.0)
            scored_results.append(result)
        
        # Sort by personalized score
        scored_results.sort(key=lambda x: x.get("personalized_score", 0), reverse=True)
        
        return scored_results[:limit]
        
    except Exception as e:
        logger.error(f"Personalization error: {e}")
        return results[:limit]


@router.post("/message")
async def chat_message(
    req: ChatRequest,
    request: Request,
    current_user: Optional[UserResponse] = Depends(get_optional_user)
):
    """
    Chat endpoint with personalization support.
    
    - **session_id**: Conversation session ID
    - **message**: User's message
    - **include_search**: Whether to include product search
    - **use_personalization**: Apply user preferences (requires authentication)
    """
    search_results = None
    
    if req.include_search:
        engine = FashionSearchEngine(request.app.state.ml_loader)
        
        # Get more results for personalization
        k = 20 if (current_user and req.use_personalization) else 5
        results = engine.search(text=req.message, k=k)
        search_results = [r.__dict__ for r in results]
        
        # ✅ Apply personalization if user is authenticated
        if current_user and req.use_personalization:
            search_results = await personalize_search_results(
                search_results,
                current_user.user_id,
                limit=10
            )
            logger.info(f"✅ Personalized results for user: {current_user.email}")
        
        # Save to search history if authenticated
        if current_user:
            try:
                history_collection = get_history_collection()
                await history_collection.insert_one({
                    "user_id": current_user.user_id,
                    "query": req.message,
                    "timestamp": datetime.utcnow(),
                    "results_count": len(search_results),
                    "session_id": req.session_id
                })
            except Exception as e:
                logger.error(f"Failed to save search history: {e}")
    
    # Generate chat response
    response = chat_service.chat(req.session_id, req.message, search_results)
    
    return {
        "response": response,
        "products": search_results,
        "personalized": bool(current_user and req.use_personalization)
    }


@router.post("/rag")
async def chat_rag(
    req: RAGRequest,
    request: Request,
    current_user: Optional[UserResponse] = Depends(get_optional_user)
):
    """
    RAG-based chat with personalization.
    
    - **query**: User's query
    - **top_k**: Number of products to retrieve
    - **use_cache**: Use cached responses
    - **use_personalization**: Apply user preferences
    """
    engine = FashionSearchEngine(request.app.state.ml_loader)
    
    # Get more results for personalization
    k = req.top_k * 2 if (current_user and req.use_personalization) else req.top_k
    search_results = engine.search(text=req.query, k=k)
    products = [r.__dict__ for r in search_results]
    
    # ✅ Apply personalization
    if current_user and req.use_personalization:
        products = await personalize_search_results(
            products,
            current_user.user_id,
            limit=req.top_k
        )
    
    # Generate RAG response
    rag_result = rag_pipeline.query(req.query, products, use_cache=req.use_cache)
    
    # Save to history
    if current_user:
        try:
            history_collection = get_history_collection()
            await history_collection.insert_one({
                "user_id": current_user.user_id,
                "query": req.query,
                "timestamp": datetime.utcnow(),
                "results_count": len(products),
                "query_type": "rag"
            })
        except Exception as e:
            logger.error(f"Failed to save RAG history: {e}")
    
    return {
        "query": req.query,
        "answer": rag_result['answer'],
        "products": rag_result['products'],
        "response_time": rag_result['response_time'],
        "cached": rag_result['cached'],
        "personalized": bool(current_user and req.use_personalization)
    }


@router.get("/rag/stats")
async def rag_stats():
    """Get RAG pipeline statistics."""
    return rag_pipeline.get_stats()


# ==================== AGENT ENDPOINTS (v2.3) ====================

class AgentRequest(BaseModel):
    """Agent request with personalization."""
    session_id: str
    query: str
    use_memory: bool = True
    use_personalization: bool = True  # ✅ NEW


@router.post("/agent/query")
async def agent_query(
    req: AgentRequest,
    request: Request,
    current_user: Optional[UserResponse] = Depends(get_optional_user)
):
    """
    Query using ReAct agent with tool calling, memory, and personalization.
    
    - **session_id**: Agent session ID
    - **query**: User's query
    - **use_memory**: Use conversation memory
    - **use_personalization**: Apply user preferences
    """
    import pandas as pd
    
    # Initialize agent for session if needed
    if req.session_id not in _agents:
        engine = FashionSearchEngine(request.app.state.ml_loader)
        products_df = pd.read_csv("data/meta_ssot.csv")
        memory = ConversationMemory(max_turns=10, summarize_threshold=5)
        
        _agents[req.session_id] = FashionAgent(
            search_engine=engine,
            products_df=products_df,
            max_iterations=5,
            memory=memory
        )
    
    agent = _agents[req.session_id]
    
    # ✅ Add user context if authenticated
    user_context = None
    if current_user and req.use_personalization:
        try:
            profiles_collection = get_profiles_collection()
            profile = await profiles_collection.find_one({"user_id": current_user.user_id})
            
            if profile:
                user_context = {
                    "user_id": current_user.user_id,
                    "style": profile.get("style", []),
                    "colors": profile.get("colors", []),
                    "size": profile.get("size")
                }
        except Exception as e:
            logger.error(f"Failed to load user context: {e}")
    
    # Run agent with user context
    result = agent.run(req.query, use_memory=req.use_memory, user_context=user_context)
    
    # Save to history
    if current_user:
        try:
            history_collection = get_history_collection()
            await history_collection.insert_one({
                "user_id": current_user.user_id,
                "query": req.query,
                "timestamp": datetime.utcnow(),
                "session_id": req.session_id,
                "query_type": "agent"
            })
        except Exception as e:
            logger.error(f"Failed to save agent history: {e}")
    
    return {
        "session_id": req.session_id,
        "query": req.query,
        "response": result.response,
        "reasoning": result.reasoning,
        "actions_taken": [{"tool": a.tool.value, "input": a.input} for a in result.actions_taken],
        "used_memory": result.used_memory,
        "response_time": result.response_time,
        "personalized": bool(current_user and req.use_personalization)
    }


@router.get("/agent/memory/{session_id}")
async def agent_memory_stats(session_id: str):
    """Get conversation memory statistics for session."""
    if session_id not in _agents:
        return {"error": "Session not found"}
    
    agent = _agents[session_id]
    return agent.get_memory_stats()


@router.post("/agent/memory/{session_id}/clear")
async def agent_memory_clear(session_id: str):
    """Clear conversation memory for session."""
    if session_id not in _agents:
        return {"error": "Session not found"}
    
    agent = _agents[session_id]
    agent.clear_memory()
    return {"status": "Memory cleared"}


@router.get("/agent/sessions")
async def agent_sessions():
    """List active agent sessions."""
    sessions = []
    for sid, agent in _agents.items():
        sessions.append({
            "session_id": sid,
            "memory_stats": agent.get_memory_stats()
        })
    return {"active_sessions": sessions, "total": len(sessions)}
