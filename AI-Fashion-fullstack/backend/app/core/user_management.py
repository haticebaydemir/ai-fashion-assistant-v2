"""User management system with profile, history, and favorites tracking."""

import json
import threading
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict


@dataclass
class UserProfile:
    """User profile with preferences and statistics."""
    user_id: str
    name: str
    email: str
    style: List[str] = field(default_factory=list)  # ["casual", "sporty"]
    size: str = ""
    colors: List[str] = field(default_factory=list)  # ["blue", "white"]
    categories: List[str] = field(default_factory=list)
    created_at: str = ""
    last_active: str = ""
    total_searches: int = 0
    total_favorites: int = 0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SearchEntry:
    """Search history entry."""
    query: str
    timestamp: str
    results_count: int = 0
    top_result_id: Optional[str] = None
    response_time: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class FavoriteProduct:
    """Favorite product entry."""
    product_id: str
    product_name: str
    category: str
    added_at: str
    view_count: int = 1
    last_viewed: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


class ThreadSafeJSONStorage:
    """Thread-safe JSON file storage."""
    
    def __init__(self):
        self.lock = threading.Lock()
    
    def load(self, filepath: Path) -> Dict:
        """Load JSON file."""
        with self.lock:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
    
    def save(self, filepath: Path, data: Dict) -> None:
        """Save JSON file."""
        with self.lock:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)


class UserProfileManager:
    """Manage user profiles."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.storage = ThreadSafeJSONStorage()
        self.profiles_file = base_dir / "users.json"
    
    def create_profile(self, user_id: str, name: str, email: str, 
                      style: List[str] = None, size: str = "", 
                      colors: List[str] = None) -> UserProfile:
        """Create new user profile."""
        profile = UserProfile(
            user_id=user_id,
            name=name,
            email=email,
            style=style or [],
            size=size,
            colors=colors or [],
            created_at=datetime.now().isoformat(),
            last_active=datetime.now().isoformat()
        )
        
        profiles = self.storage.load(self.profiles_file)
        profiles[user_id] = profile.to_dict()
        self.storage.save(self.profiles_file, profiles)
        
        return profile
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile."""
        profiles = self.storage.load(self.profiles_file)
        if user_id in profiles:
            data = profiles[user_id]
            return UserProfile(
                user_id=data['user_id'],
                name=data['name'],
                email=data['email'],
                style=data.get('style', []),
                size=data.get('size', ''),
                colors=data.get('colors', []),
                categories=data.get('categories', []),
                created_at=data.get('created_at', ''),
                last_active=data.get('last_active', ''),
                total_searches=data.get('total_searches', 0),
                total_favorites=data.get('total_favorites', 0)
            )
        return None
    
    def update_profile(self, user_id: str, **kwargs) -> Optional[UserProfile]:
        """Update user profile."""
        profile = self.get_profile(user_id)
        if not profile:
            return None
        
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        profile.last_active = datetime.now().isoformat()
        profiles = self.storage.load(self.profiles_file)
        profiles[user_id] = profile.to_dict()
        self.storage.save(self.profiles_file, profiles)
        
        return profile
    
    def list_profiles(self) -> List[UserProfile]:
        """List all user profiles."""
        profiles = self.storage.load(self.profiles_file)
        result = []
        for user_id, data in profiles.items():
            result.append(UserProfile(
                user_id=data['user_id'],
                name=data['name'],
                email=data['email'],
                style=data.get('style', []),
                size=data.get('size', ''),
                colors=data.get('colors', []),
                categories=data.get('categories', []),
                created_at=data.get('created_at', ''),
                last_active=data.get('last_active', ''),
                total_searches=data.get('total_searches', 0),
                total_favorites=data.get('total_favorites', 0)
            ))
        return result


class SearchHistoryManager:
    """Manage search history per user."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.storage = ThreadSafeJSONStorage()
    
    def add_search(self, user_id: str, query: str, results_count: int = 0,
                   top_result_id: Optional[str] = None, response_time: float = 0.0) -> SearchEntry:
        """Add search to user history."""
        entry = SearchEntry(
            query=query,
            timestamp=datetime.now().isoformat(),
            results_count=results_count,
            top_result_id=top_result_id,
            response_time=response_time
        )
        
        history_file = self.base_dir / f"history_{user_id}.json"
        history = self.storage.load(history_file)
        
        if 'searches' not in history:
            history['searches'] = []
        
        history['searches'].append(entry.to_dict())
        self.storage.save(history_file, history)
        
        return entry
    
    def get_history(self, user_id: str) -> List[SearchEntry]:
        """Get search history for user."""
        history_file = self.base_dir / f"history_{user_id}.json"
        history = self.storage.load(history_file)
        
        result = []
        for entry_data in history.get('searches', []):
            result.append(SearchEntry(
                query=entry_data['query'],
                timestamp=entry_data['timestamp'],
                results_count=entry_data.get('results_count', 0),
                top_result_id=entry_data.get('top_result_id'),
                response_time=entry_data.get('response_time', 0.0)
            ))
        return result
    
    def get_top_queries(self, user_id: str, n: int = 5) -> List[str]:
        """Get top N most frequent queries."""
        history = self.get_history(user_id)
        query_counts = defaultdict(int)
        
        for entry in history:
            query_counts[entry.query] += 1
        
        sorted_queries = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)
        return [q for q, _ in sorted_queries[:n]]
    
    def get_analytics(self, user_id: str) -> Dict:
        """Get search analytics for user."""
        history = self.get_history(user_id)
        
        if not history:
            return {
                "total_searches": 0,
                "avg_response_time": 0,
                "unique_queries": 0
            }
        
        avg_response_time = sum(e.response_time for e in history) / len(history)
        unique_queries = len(set(e.query for e in history))
        
        return {
            "total_searches": len(history),
            "avg_response_time": avg_response_time,
            "unique_queries": unique_queries,
            "top_queries": self.get_top_queries(user_id, 3)
        }


class FavoritesManager:
    """Manage favorite products per user."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.storage = ThreadSafeJSONStorage()
    
    def add_favorite(self, user_id: str, product_id: str, product_name: str, 
                     category: str) -> FavoriteProduct:
        """Add product to user favorites."""
        favorite = FavoriteProduct(
            product_id=product_id,
            product_name=product_name,
            category=category,
            added_at=datetime.now().isoformat(),
            last_viewed=datetime.now().isoformat()
        )
        
        favorites_file = self.base_dir / f"favorites_{user_id}.json"
        favorites = self.storage.load(favorites_file)
        
        if 'favorites' not in favorites:
            favorites['favorites'] = []
        
        # Check if already favorited
        for fav in favorites['favorites']:
            if fav['product_id'] == product_id:
                fav['view_count'] = fav.get('view_count', 1) + 1
                fav['last_viewed'] = datetime.now().isoformat()
                self.storage.save(favorites_file, favorites)
                return favorite
        
        favorites['favorites'].append(favorite.to_dict())
        self.storage.save(favorites_file, favorites)
        
        return favorite
    
    def remove_favorite(self, user_id: str, product_id: str) -> bool:
        """Remove product from favorites."""
        favorites_file = self.base_dir / f"favorites_{user_id}.json"
        favorites = self.storage.load(favorites_file)
        
        if 'favorites' not in favorites:
            return False
        
        original_count = len(favorites['favorites'])
        favorites['favorites'] = [f for f in favorites['favorites'] 
                                 if f['product_id'] != product_id]
        
        if len(favorites['favorites']) < original_count:
            self.storage.save(favorites_file, favorites)
            return True
        return False
    
    def get_favorites(self, user_id: str) -> List[FavoriteProduct]:
        """Get user favorites."""
        favorites_file = self.base_dir / f"favorites_{user_id}.json"
        favorites = self.storage.load(favorites_file)
        
        result = []
        for fav_data in favorites.get('favorites', []):
            result.append(FavoriteProduct(
                product_id=fav_data['product_id'],
                product_name=fav_data['product_name'],
                category=fav_data['category'],
                added_at=fav_data['added_at'],
                view_count=fav_data.get('view_count', 1),
                last_viewed=fav_data.get('last_viewed', '')
            ))
        return result
    
    def get_favorite_categories(self, user_id: str) -> Dict[str, int]:
        """Get category distribution of favorites."""
        favorites = self.get_favorites(user_id)
        categories = defaultdict(int)
        
        for fav in favorites:
            categories[fav.category] += 1
        
        return dict(categories)


class UserManager:
    """Unified user management system."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.profile_manager = UserProfileManager(self.base_dir)
        self.history_manager = SearchHistoryManager(self.base_dir)
        self.favorites_manager = FavoritesManager(self.base_dir)
    
    def get_user_full_data(self, user_id: str) -> Dict:
        """Get complete user data."""
        profile = self.profile_manager.get_profile(user_id)
        if not profile:
            return {}
        
        history = self.history_manager.get_history(user_id)
        favorites = self.favorites_manager.get_favorites(user_id)
        search_analytics = self.history_manager.get_analytics(user_id)
        favorite_categories = self.favorites_manager.get_favorite_categories(user_id)
        
        return {
            "profile": profile.to_dict(),
            "search_history": [h.to_dict() for h in history],
            "favorites": [f.to_dict() for f in favorites],
            "search_analytics": search_analytics,
            "favorite_categories": favorite_categories
        }
