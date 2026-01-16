"""
AI Fashion Assistant Backend - Updated with MongoDB Authentication
Main FastAPI application with user authentication and personalization.
"""
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

# Import database
from app.database import Database

# Import API routers
from app.api.endpoints import auth, chat_updated as chat, search_updated as search, users_updated as users

# Import ML loader (existing)
from app.core.ml_loader import MLLoader

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events: startup and shutdown.
    """
    # ==================== STARTUP ====================
    logger.info("🚀 Starting AI Fashion Assistant Backend...")
    
    # 1. Connect to MongoDB
    try:
        await Database.connect_db()
        logger.info("✅ MongoDB connected successfully")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        logger.warning("⚠️ Running without database - authentication will not work!")
    
    # 2. Initialize ML models
    try:
        ml_loader = MLLoader()
        # MLLoader automatically loads on initialization
        app.state.ml_loader = ml_loader
        app.mount("/images", StaticFiles(directory="data/images"), name="images")
        logger.info("✅ ML models loaded successfully")
    except Exception as e:
        logger.error(f"❌ ML model loading failed: {e}")
        logger.warning("⚠️ Search functionality will be limited without embeddings")
        app.state.ml_loader = None
    
    logger.info("✅ Application startup complete!")
    
    yield
    
    # ==================== SHUTDOWN ====================
    logger.info("🛑 Shutting down AI Fashion Assistant Backend...")
    
    # Close MongoDB connection
    await Database.close_db()
    
    logger.info("✅ Application shutdown complete!")


# Create FastAPI app
app = FastAPI(
    title="AI Fashion Assistant API",
    description="Complete fashion search system with authentication and personalization",
    version="2.5.0",
    lifespan=lifespan
)

# ==================== CORS CONFIGURATION ====================
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== STATIC FILES ====================
# Serve product images
if os.path.exists("data/images"):
    app.mount("/images", StaticFiles(directory="data/images"), name="images")

# ==================== API ROUTES ====================

# Authentication routes
app.include_router(auth.router, prefix="/api", tags=["Authentication"])

# Search routes
app.include_router(search.router, prefix="/api/search", tags=["Search"])

# Chat routes
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

# User routes
app.include_router(users.router, prefix="/api/users", tags=["Users"])


# ==================== ROOT ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "AI Fashion Assistant API",
        "version": "2.5.0",
        "status": "running",
        "features": [
            "JWT Authentication",
            "User Management",
            "Text Search",
            "Image Search",
            "Multimodal Search",
            "RAG-based Chat",
            "AI Agents with Memory",
            "Personalization Engine",
            "Favorites & History"
        ],
        "endpoints": {
            "auth": "/api/auth",
            "search": "/api/search",
            "chat": "/api/chat",
            "users": "/api/users",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check MongoDB
        db_status = "connected" if Database.db else "disconnected"
        
        # Check ML models
        ml_status = "loaded" if app.state.ml_loader else "not loaded"
        
        return {
            "status": "healthy",
            "database": db_status,
            "ml_models": ml_status,
            "version": "2.5.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.get("/api/info")
async def api_info():
    """Detailed API information."""
    return {
        "api_version": "2.5.0",
        "features": {
            "authentication": {
                "type": "JWT",
                "endpoints": [
                    "POST /api/auth/register",
                    "POST /api/auth/login",
                    "POST /api/auth/refresh",
                    "POST /api/auth/logout",
                    "GET /api/auth/me"
                ]
            },
            "search": {
                "types": ["text", "image", "multimodal"],
                "personalization": True,
                "endpoints": [
                    "POST /api/search/text",
                    "POST /api/search/image",
                    "POST /api/search/multimodal",
                    "POST /api/search/rag"
                ]
            },
            "chat": {
                "features": ["RAG", "Memory", "Tools", "Personalization"],
                "endpoints": [
                    "POST /api/chat/message",
                    "POST /api/chat/rag",
                    "POST /api/chat/agent/query"
                ]
            },
            "user_features": {
                "profile": True,
                "favorites": True,
                "history": True,
                "recommendations": True,
                "endpoints": [
                    "GET/PUT /api/users/{user_id}/profile",
                    "GET/POST/DELETE /api/users/{user_id}/favorites",
                    "GET/DELETE /api/users/{user_id}/history",
                    "POST /api/users/{user_id}/recommendations"
                ]
            }
        },
        "database": "MongoDB",
        "ml_models": {
            "text": "MPNet (sentence-transformers)",
            "image": "CLIP (OpenAI)",
            "llm": "Llama-3.3-70B (GROQ)"
        }
    }


# ==================== ERROR HANDLERS ====================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return {
        "error": "Not Found",
        "message": "The requested endpoint does not exist",
        "available_endpoints": {
            "docs": "/docs",
            "health": "/health",
            "api_info": "/api/info"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    
    logger.info(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   🛍️  AI Fashion Assistant Backend v2.5                 ║
    ║                                                          ║
    ║   📡 Server: http://localhost:{port}                       ║
    ║   📚 Docs:   http://localhost:{port}/docs                 ║
    ║   💾 DB:     MongoDB                                     ║
    ║   🔐 Auth:   JWT                                         ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )