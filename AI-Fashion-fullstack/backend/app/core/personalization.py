"""Content-based personalization engine with multi-strategy recommendations."""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


@dataclass
class RecommendationResult:
    """Recommendation result with strategy breakdown."""
    product_id: str
    product_name: str
    score: float
    strategy: str  # "favorites", "history", "preferences"
    reasoning: str


class PreferenceEncoder:
    """Encode user preferences into vectors."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def encode_preferences(self, preferences: Dict[str, List[str]]) -> np.ndarray:
        """Encode user preferences to vector."""
        # Create preference text
        style_text = ", ".join(preferences.get("style", [])) or "general"
        colors_text = ", ".join(preferences.get("colors", [])) or "any color"
        categories_text = ", ".join(preferences.get("categories", [])) or "all categories"
        
        preference_str = f"I like {style_text} style clothing in {colors_text} from {categories_text}"
        
        # Encode to vector
        embedding = self.model.encode(preference_str, convert_to_numpy=True)
        return embedding
    
    def encode_product_metadata(self, product: Dict[str, Any]) -> np.ndarray:
        """Encode product metadata to vector."""
        name = product.get("product_name", "")
        category = product.get("category", "")
        color = product.get("color", "")
        
        product_str = f"{name} is a {category} in {color}"
        
        embedding = self.model.encode(product_str, convert_to_numpy=True)
        return embedding


class ContentBasedRecommender:
    """Content-based recommendation system."""
    
    def __init__(self, products_df: Any, preference_encoder: PreferenceEncoder):
        """
        Initialize recommender.
        
        Args:
            products_df: DataFrame with product information
            preference_encoder: PreferenceEncoder instance
        """
        self.products_df = products_df
        self.encoder = preference_encoder
        self.embeddings_cache = {}
    
    def _get_product_embedding(self, product_id: str) -> Optional[np.ndarray]:
        """Get or compute product embedding."""
        if product_id in self.embeddings_cache:
            return self.embeddings_cache[product_id]
        
        # Find product in dataframe
        product_mask = self.products_df['product_id'] == product_id
        if not product_mask.any():
            return None
        
        product = self.products_df[product_mask].iloc[0]
        product_dict = product.to_dict() if hasattr(product, 'to_dict') else dict(product)
        
        embedding = self.encoder.encode_product_metadata(product_dict)
        self.embeddings_cache[product_id] = embedding
        
        return embedding
    
    def recommend_from_favorites(self, favorites: List[Dict], n: int = 10, 
                                 exclude_ids: List[str] = None) -> List[RecommendationResult]:
        """Recommend products similar to user's favorites."""
        if not favorites:
            return []
        
        exclude_ids = exclude_ids or []
        favorite_ids = [f.get('product_id') for f in favorites]
        
        # Get embeddings for favorites
        favorite_embeddings = []
        for fav_id in favorite_ids:
            emb = self._get_product_embedding(fav_id)
            if emb is not None:
                favorite_embeddings.append(emb)
        
        if not favorite_embeddings:
            return []
        
        # Average embedding of favorites
        favorite_avg = np.mean(favorite_embeddings, axis=0)
        
        # Score all products
        results = []
        for product_id in self.products_df['product_id']:
            if product_id in exclude_ids or product_id in favorite_ids:
                continue
            
            product_emb = self._get_product_embedding(product_id)
            if product_emb is None:
                continue
            
            similarity = cosine_similarity([favorite_avg], [product_emb])[0][0]
            
            product = self.products_df[self.products_df['product_id'] == product_id].iloc[0]
            product_dict = product.to_dict() if hasattr(product, 'to_dict') else dict(product)
            
            results.append(RecommendationResult(
                product_id=str(product_id),
                product_name=product_dict.get('product_name', 'Unknown'),
                score=float(similarity),
                strategy="favorites",
                reasoning=f"Similar to your favorite {product_dict.get('category', 'items')}"
            ))
        
        # Sort and return top N
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:n]
    
    def recommend_from_history(self, search_queries: List[str], n: int = 10,
                              exclude_ids: List[str] = None) -> List[RecommendationResult]:
        """Recommend products based on search history."""
        if not search_queries:
            return []
        
        exclude_ids = exclude_ids or []
        
        # Encode search queries
        query_embeddings = [self.encoder.model.encode(q, convert_to_numpy=True) 
                           for q in search_queries]
        query_avg = np.mean(query_embeddings, axis=0)
        
        # Score all products
        results = []
        for product_id in self.products_df['product_id']:
            if product_id in exclude_ids:
                continue
            
            product_emb = self._get_product_embedding(product_id)
            if product_emb is None:
                continue
            
            similarity = cosine_similarity([query_avg], [product_emb])[0][0]
            
            product = self.products_df[self.products_df['product_id'] == product_id].iloc[0]
            product_dict = product.to_dict() if hasattr(product, 'to_dict') else dict(product)
            
            results.append(RecommendationResult(
                product_id=str(product_id),
                product_name=product_dict.get('product_name', 'Unknown'),
                score=float(similarity),
                strategy="history",
                reasoning=f"Based on your search for {search_queries[0]}"
            ))
        
        # Sort and return top N
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:n]
    
    def recommend_from_preferences(self, preferences: Dict, n: int = 10,
                                  exclude_ids: List[str] = None) -> List[RecommendationResult]:
        """Recommend products matching user preferences."""
        exclude_ids = exclude_ids or []
        
        # Encode preferences
        pref_embedding = self.encoder.encode_preferences(preferences)
        
        # Filter by hard constraints (size, colors, categories)
        size = preferences.get("size", "")
        colors = preferences.get("colors", [])
        categories = preferences.get("categories", [])
        
        # Score all products
        results = []
        for product_id in self.products_df['product_id']:
            if product_id in exclude_ids:
                continue
            
            product = self.products_df[self.products_df['product_id'] == product_id].iloc[0]
            product_dict = product.to_dict() if hasattr(product, 'to_dict') else dict(product)
            
            # Get embedding
            product_emb = self._get_product_embedding(product_id)
            if product_emb is None:
                continue
            
            # Soft matching on preferences
            similarity = cosine_similarity([pref_embedding], [product_emb])[0][0]
            
            # Boost score if color matches
            if colors and product_dict.get('color', '').lower() in [c.lower() for c in colors]:
                similarity *= 1.2
            
            # Boost score if category matches
            if categories and product_dict.get('category', '').lower() in [c.lower() for c in categories]:
                similarity *= 1.15
            
            results.append(RecommendationResult(
                product_id=str(product_id),
                product_name=product_dict.get('product_name', 'Unknown'),
                score=float(similarity),
                strategy="preferences",
                reasoning=f"Matches your preference for {preferences.get('style', ['general'])[0]} style"
            ))
        
        # Sort and return top N
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:n]


class PersonalizationEngine:
    """Multi-strategy personalization engine."""
    
    def __init__(self, products_df: Any):
        """
        Initialize personalization engine.
        
        Args:
            products_df: DataFrame with product information
        """
        self.products_df = products_df
        self.preference_encoder = PreferenceEncoder()
        self.recommender = ContentBasedRecommender(products_df, self.preference_encoder)
        
        # Strategy weights
        self.weights = {
            "favorites": 0.50,
            "history": 0.30,
            "preferences": 0.20
        }
    
    def recommend_for_user(self, user_id: str, user_data: Dict, n: int = 20,
                          top_per_strategy: int = 10) -> Dict[str, List[RecommendationResult]]:
        """
        Generate personalized recommendations for user.
        
        Args:
            user_id: User ID
            user_data: User data dict with profile, favorites, search_history
            n: Total recommendations to return
            top_per_strategy: Top items per strategy before aggregation
        
        Returns:
            Dict with 'from_favorites', 'from_history', 'from_preferences', 'combined'
        """
        profile = user_data.get("profile", {})
        favorites = user_data.get("favorites", [])
        search_history = user_data.get("search_history", [])
        
        exclude_ids = [f['product_id'] for f in favorites]
        
        # Get recommendations from each strategy
        from_fav = self.recommender.recommend_from_favorites(
            favorites, n=top_per_strategy, exclude_ids=exclude_ids
        ) if favorites else []
        
        search_queries = [s['query'] for s in search_history[-5:]] if search_history else []
        from_hist = self.recommender.recommend_from_history(
            search_queries, n=top_per_strategy, exclude_ids=exclude_ids
        ) if search_queries else []
        
        preferences = {
            "style": profile.get("style", []),
            "colors": profile.get("colors", []),
            "categories": profile.get("categories", [])
        }
        from_pref = self.recommender.recommend_from_preferences(
            preferences, n=top_per_strategy, exclude_ids=exclude_ids
        ) if any(preferences.values()) else []
        
        # Aggregate with weights
        combined = self._aggregate_recommendations(
            from_fav, from_hist, from_pref, n=n
        )
        
        return {
            "from_favorites": from_fav[:top_per_strategy],
            "from_history": from_hist[:top_per_strategy],
            "from_preferences": from_pref[:top_per_strategy],
            "combined": combined[:n]
        }
    
    def _aggregate_recommendations(self, fav_recs: List[RecommendationResult],
                                  hist_recs: List[RecommendationResult],
                                  pref_recs: List[RecommendationResult],
                                  n: int = 20) -> List[RecommendationResult]:
        """Aggregate recommendations from all strategies."""
        # Create score dict
        scores = {}
        
        for rec in fav_recs:
            scores[rec.product_id] = scores.get(rec.product_id, 0) + rec.score * self.weights["favorites"]
        
        for rec in hist_recs:
            scores[rec.product_id] = scores.get(rec.product_id, 0) + rec.score * self.weights["history"]
        
        for rec in pref_recs:
            scores[rec.product_id] = scores.get(rec.product_id, 0) + rec.score * self.weights["preferences"]
        
        # Create combined results
        combined = []
        all_recs = {rec.product_id: rec for rec in fav_recs + hist_recs + pref_recs}
        
        for product_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]:
            rec = all_recs[product_id]
            combined.append(RecommendationResult(
                product_id=rec.product_id,
                product_name=rec.product_name,
                score=float(score),
                strategy="combined",
                reasoning=f"Recommended based on your favorites, search history, and preferences"
            ))
        
        return combined
    
    def get_metrics(self, recommendations: Dict[str, List[RecommendationResult]],
                   products_df: Any = None) -> Dict:
        """Calculate personalization metrics."""
        combined = recommendations.get("combined", [])
        
        if not combined:
            return {
                "coverage": 0.0,
                "diversity": 0.0,
                "avg_score": 0.0
            }
        
        # Coverage: unique products / total available
        unique_products = len(set(r.product_id for r in combined))
        total_products = len(products_df) if products_df is not None else 1
        coverage = unique_products / max(total_products, 1)
        
        # Diversity: category distribution
        if products_df is not None:
            categories = []
            for rec in combined:
                mask = products_df['product_id'] == rec.product_id
                if mask.any():
                    cat = products_df[mask].iloc[0].get('category', 'Unknown')
                    categories.append(cat)
            
            unique_categories = len(set(categories))
            diversity = unique_categories / len(combined) if combined else 0
        else:
            diversity = 0.0
        
        # Avg score
        avg_score = np.mean([r.score for r in combined]) if combined else 0.0
        
        return {
            "coverage": float(coverage),
            "diversity": float(diversity),
            "avg_score": float(avg_score),
            "unique_products": unique_products,
            "avg_score_description": "Average recommendation score (0-1)"
        }
