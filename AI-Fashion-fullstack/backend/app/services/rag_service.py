from groq import Groq
from typing import List, Dict, Optional, Tuple
from app.core.config import settings
import logging
import json
import time
from pathlib import Path
from collections import defaultdict

logger = logging.getLogger(__name__)

class FashionRAGPipeline:
    """Production-ready RAG pipeline for fashion search with caching and batch support (v2.2)."""
    
    def __init__(self, cache_dir: Optional[Path] = None, enable_cache: bool = True):
        self.client = Groq(api_key=settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None
        self.cache_dir = Path(cache_dir or "data/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "rag_cache.json"
        self.enable_cache = enable_cache
        self.cache = self._load_cache()
        self.stats = {
            'total_queries': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_response_time': 0.0,
            'response_times': [],
            'query_log': []
        }
    
    def _load_cache(self) -> Dict:
        if self.cache_file.exists():
            try:
                return json.load(open(self.cache_file, 'r', encoding='utf8'))
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
        return {}
    
    def _save_cache(self):
        if self.enable_cache:
            try:
                json.dump(self.cache, open(self.cache_file, 'w', encoding='utf8'))
            except Exception as e:
                logger.warning(f"Failed to save cache: {e}")
    
    def _get_cache_key(self, query: str, top_k: int = 5) -> str:
        return f"{query}::{top_k}".lower()
    
    def _build_context(self, products: List[dict], max_products: int = 5) -> str:
        context = "Top matching products:\n"
        for i, p in enumerate(products[:max_products], 1):
            product_name = p.get('product_name', 'Unknown')
            category = p.get('category', 'Unknown')
            color = p.get('color', 'Unknown')
            gender = p.get('gender', 'Unknown')
            score = p.get('score', 0.0)
            context += f"{i}. {product_name} (Category: {category}, Color: {color}, Gender: {gender}, Match: {score:.2f})\n"
        return context
    
    def query(self, query: str, products: List[dict], use_cache: bool = True, 
              temperature: float = 0.1, max_tokens: int = 500) -> Dict:
        """Generate RAG response for a single query."""
        cache_key = self._get_cache_key(query)
        start_time = time.time()
        
        # Check cache
        if use_cache and cache_key in self.cache:
            self.stats['cache_hits'] += 1
            logger.info(f"Cache hit for: {query}")
            return {
                'query': query,
                'answer': self.cache[cache_key]['answer'],
                'products': products[:5],
                'cached': True,
                'response_time': time.time() - start_time
            }
        
        # Cache miss
        self.stats['cache_misses'] += 1
        
        if not self.client:
            return {
                'query': query,
                'answer': "RAG service not configured (no GROQ_API_KEY).",
                'products': products[:5],
                'cached': False,
                'response_time': time.time() - start_time,
                'error': True
            }
        
        context = self._build_context(products)
        
        try:
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional fashion assistant. Provide a natural language recommendation based on the products provided. Be concise and helpful."
                    },
                    {
                        "role": "user",
                        "content": f"User query: {query}\n\n{context}\n\nBased on these products, provide a helpful fashion recommendation in 2-3 sentences."
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            answer = response.choices[0].message.content
            response_time = time.time() - start_time
            
            # Cache the result
            self.cache[cache_key] = {'answer': answer, 'timestamp': time.time()}
            self._save_cache()
            
            self.stats['total_queries'] += 1
            self.stats['total_response_time'] += response_time
            self.stats['response_times'].append(response_time)
            self.stats['query_log'].append({'query': query, 'time': response_time, 'cached': False})
            
            return {
                'query': query,
                'answer': answer,
                'products': products[:5],
                'cached': False,
                'response_time': response_time
            }
        except Exception as e:
            logger.error(f"RAG generation error: {e}")
            response_time = time.time() - start_time
            self.stats['total_queries'] += 1
            self.stats['total_response_time'] += response_time
            return {
                'query': query,
                'answer': f"Error generating response: {str(e)}",
                'products': products[:5],
                'cached': False,
                'response_time': response_time,
                'error': True
            }
    
    def batch_query(self, queries: List[str], products_list: List[List[dict]], 
                    use_cache: bool = True) -> List[Dict]:
        """Process multiple queries sequentially."""
        results = []
        for query, products in zip(queries, products_list):
            result = self.query(query, products, use_cache=use_cache)
            results.append(result)
        return results
    
    def get_stats(self) -> Dict:
        """Return RAG pipeline statistics."""
        stats = self.stats.copy()
        if stats['total_queries'] > 0:
            stats['avg_response_time'] = stats['total_response_time'] / (stats['total_queries'] - stats['cache_hits'])
            stats['cache_hit_rate'] = stats['cache_hits'] / (stats['cache_hits'] + stats['cache_misses']) if (stats['cache_hits'] + stats['cache_misses']) > 0 else 0.0
        else:
            stats['avg_response_time'] = 0.0
            stats['cache_hit_rate'] = 0.0
        return stats


# Legacy alias for backward compatibility
class RAGService(FashionRAGPipeline):
    """Backward-compatible RAG service."""
    def __init__(self):
        super().__init__(enable_cache=True)
    
    def generate_response(self, query: str, products: List[dict]) -> str:
        result = self.query(query, products)
        return result.get('answer', '')
