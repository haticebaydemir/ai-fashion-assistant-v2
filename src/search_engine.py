"""
Baseline Fashion Search Engine

Production-grade search engine supporting:
- Text search (mpnet + CLIP text)
- Image search (CLIP image)
- Hybrid search (text + image)
- Query understanding and filtering
- FAISS-based retrieval
"""

import numpy as np
import pandas as pd
import faiss
import torch
from typing import List, Dict, Optional, Tuple, Union
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
from transformers import CLIPModel, CLIPProcessor
from PIL import Image
import re

try:
    from schema import normalize_text
except ImportError:
    def normalize_text(text: str, mode: str = "standard") -> str:
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        return text


@dataclass
class QueryIntent:
    """Query intent classification"""
    query_type: str
    search_mode: str
    normalized_text: Optional[str] = None
    has_filters: bool = False
    filters: Dict = None


@dataclass
class SearchResult:
    """Search result with ranking information"""
    rank: int
    product_id: int
    product_name: str
    category: str
    gender: str
    color: str
    distance: float
    similarity: float
    score: float


class QueryUnderstanding:
    """Query understanding and normalization"""
    
    def __init__(self):
        self.category_keywords = {
            'apparel': ['dress', 'shirt', 'tshirt', 'jeans', 'pants'],
            'accessories': ['watch', 'bag', 'wallet', 'belt'],
            'footwear': ['shoes', 'sandals', 'heels', 'boots']
        }
        self.color_keywords = [
            'red', 'blue', 'green', 'yellow', 'black', 'white',
            'grey', 'pink', 'purple', 'brown', 'orange'
        ]
        self.gender_keywords = ['men', 'women', 'unisex', 'boys', 'girls']
    
    def understand_query(self, text: Optional[str] = None, image: Optional[Image.Image] = None) -> QueryIntent:
        if text and image:
            query_type, search_mode = 'hybrid', 'semantic'
        elif text:
            query_type, search_mode = 'text', 'semantic'
        elif image:
            query_type, search_mode = 'image', 'visual'
        else:
            raise ValueError("Must provide text or image!")
        
        normalized_text = None
        filters = {}
        has_filters = False
        
        if text:
            normalized_text = normalize_text(text, mode="standard")
            text_lower = text.lower()
            
            for color in self.color_keywords:
                if color in text_lower:
                    filters['color'] = color
                    has_filters = True
            
            for gender in self.gender_keywords:
                if gender in text_lower:
                    filters['gender'] = gender
                    has_filters = True
        
        return QueryIntent(
            query_type=query_type,
            search_mode=search_mode,
            normalized_text=normalized_text,
            has_filters=has_filters,
            filters=filters
        )


class FashionSearchEngine:
    """Production-grade fashion search engine"""
    
    def __init__(self, index, products_df, text_model, clip_model, clip_processor, query_understander, device="cpu"):
        self.index = index
        self.df = products_df
        self.text_model = text_model
        self.clip_model = clip_model
        self.clip_processor = clip_processor
        self.query_understander = query_understander
        self.device = device
        self._embedding_cache = {}
    
    def encode_text(self, text: str) -> np.ndarray:
        if text in self._embedding_cache:
            return self._embedding_cache[text]
        
        mpnet_emb = self.text_model.encode([text], convert_to_numpy=True)[0]
        inputs = self.clip_processor(text=[text], return_tensors="pt", padding=True, truncation=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            clip_text_emb = self.clip_model.get_text_features(**inputs).cpu().numpy()[0]
        
        combined = np.concatenate([mpnet_emb, clip_text_emb])
        self._embedding_cache[text] = combined
        return combined
    
    def encode_image(self, image: Image.Image) -> np.ndarray:
        inputs = self.clip_processor(images=image, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            return self.clip_model.get_image_features(**inputs).cpu().numpy()[0]
    
    def search(self, text=None, image=None, k=50, text_weight=0.7, apply_filters=True) -> List[SearchResult]:
        intent = self.query_understander.understand_query(text=text, image=image)
        
        if text:
            text = intent.normalized_text
        
        if text and image:
            text_emb = self.encode_text(text) * text_weight
            image_emb = self.encode_image(image) * (1 - text_weight)
            hybrid_emb = np.concatenate([text_emb, image_emb])
        elif text:
            text_emb = self.encode_text(text)
            hybrid_emb = np.concatenate([text_emb, np.zeros(768)])
        elif image:
            image_emb = self.encode_image(image)
            hybrid_emb = np.concatenate([np.zeros(1536), image_emb])
        else:
            raise ValueError("Must provide text or image!")
        
        hybrid_emb = hybrid_emb / np.linalg.norm(hybrid_emb)
        query_vec = hybrid_emb.astype('float32').reshape(1, -1)
        
        retrieve_k = k * 3 if apply_filters and intent.has_filters else k
        distances, indices = self.index.search(query_vec, retrieve_k)
        
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            product = self.df.iloc[idx]
            
            if apply_filters and intent.has_filters:
                if 'color' in intent.filters:
                    if intent.filters['color'] not in str(product.get('baseColour', '')').lower():
                        continue
                if 'gender' in intent.filters:
                    if intent.filters['gender'] not in str(product.get('gender', '')').lower():
                        continue
            
            similarity = 1 - dist
            results.append(SearchResult(
                rank=len(results) + 1,
                product_id=int(product['id']),
                product_name=product['productDisplayName'],
                category=product.get('masterCategory', 'Unknown'),
                gender=product.get('gender', 'Unknown'),
                color=product.get('baseColour', 'Unknown'),
                distance=float(dist),
                similarity=float(similarity),
                score=float(similarity)
            ))
            
            if len(results) >= k:
                break
        
        return results
    
    def search_text(self, query: str, k: int = 10) -> List[SearchResult]:
        return self.search(text=query, k=k)
    
    def search_image(self, image: Image.Image, k: int = 10) -> List[SearchResult]:
        return self.search(image=image, k=k)
    
    def search_hybrid(self, query: str, image: Image.Image, k: int = 10, text_weight: float = 0.7) -> List[SearchResult]:
        return self.search(text=query, image=image, k=k, text_weight=text_weight)
