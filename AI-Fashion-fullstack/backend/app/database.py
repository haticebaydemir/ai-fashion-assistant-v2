"""MongoDB database configuration and connection management."""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Database:
    """MongoDB database manager with async support."""
    
    client: Optional[AsyncIOMotorClient] = None
    db = None
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB."""
        try:
            mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            db_name = os.getenv("MONGODB_DB_NAME", "ai_fashion_db")
            
            cls.client = AsyncIOMotorClient(
                mongodb_url,
                maxPoolSize=10,
                minPoolSize=1,
                serverSelectionTimeoutMS=5000
            )
            
            # Test connection
            await cls.client.admin.command('ping')
            cls.db = cls.client[db_name]
            
            logger.info(f"✅ Connected to MongoDB: {db_name}")
            
            # Create indexes
            await cls._create_indexes()
            
        except ConnectionFailure as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error connecting to MongoDB: {e}")
            raise
    
    @classmethod
    async def _create_indexes(cls):
        """Create database indexes for performance."""
        try:
            # Users collection indexes
            await cls.db.users.create_index("email", unique=True)
            await cls.db.users.create_index("user_id", unique=True)
            
            # User profiles index
            await cls.db.user_profiles.create_index("user_id", unique=True)
            
            # Favorites indexes
            await cls.db.favorites.create_index([("user_id", 1), ("product_id", 1)], unique=True)
            await cls.db.favorites.create_index("user_id")
            
            # Search history indexes
            await cls.db.search_history.create_index("user_id")
            await cls.db.search_history.create_index([("user_id", 1), ("timestamp", -1)])
            
            logger.info("✅ Database indexes created")
            
        except Exception as e:
            logger.warning(f"⚠️ Error creating indexes: {e}")
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")
    
    @classmethod
    def get_db(cls):
        """Get database instance."""
        if cls.db is None:
            raise RuntimeError("Database not connected. Call connect_db() first.")
        return cls.db


# Global database instance
async def get_database():
    """Dependency to get database instance."""
    return Database.get_db()


# Collections shortcuts
def get_users_collection():
    """Get users collection."""
    return Database.get_db().users


def get_profiles_collection():
    """Get user profiles collection."""
    return Database.get_db().user_profiles


def get_favorites_collection():
    """Get favorites collection."""
    return Database.get_db().favorites


def get_history_collection():
    """Get search history collection."""
    return Database.get_db().search_history
