"""Multimodal retrieval with text and image queries - v2.4.5."""

import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
import logging
from PIL import Image
import time

logger = logging.getLogger(__name__)


@dataclass
class MultimodalResult:
    """Multimodal search result."""
    product_id: int
    product_name: str
    category: str
    color: str
    text_score: float = 0.0
    image_score: float = 0.0
    fused_score: float = 0.0
    source: str = "text"  # "text", "image", or "both"
    visual_keywords: List[str] = None
    
    def __post_init__(self):
        if self.visual_keywords is None:
            self.visual_keywords = []


class ImageQueryProcessor:
    """Process image queries for multimodal search."""
    
    def __init__(self, ml_loader: Any):
        """
        Initialize image query processor.
        
        Args:
            ml_loader: MLLoader with CLIP model and processor
        """
        self.ml_loader = ml_loader
        self.processor = ml_loader.clip_processor
        self.model = ml_loader.clip_model
    
    def encode_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Encode image to embedding.
        
        Args:
            image_path: Path to image file
        
        Returns:
            CLIP image embedding (768d)
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Process with CLIP
            inputs = self.processor(images=image, return_tensors="pt")
            
            # Get embedding
            with np.warnings.catch_warnings():
                np.warnings.filterwarnings('ignore')
                image_embedding = self.model.get_image_features(**inputs)
            
            # Normalize
            embedding = image_embedding.detach().cpu().numpy()[0]
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            
            return embedding
        except Exception as e:
            logger.error(f"Error encoding image {image_path}: {e}")
            return None
    
    def encode_text_query(self, text: str) -> Optional[np.ndarray]:
        """
        Encode text query to embedding.
        
        Args:
            text: Text query
        
        Returns:
            CLIP text embedding (768d)
        """
        try:
            inputs = self.processor(text=text, return_tensors="pt")
            
            with np.warnings.catch_warnings():
                np.warnings.filterwarnings('ignore')
                text_embedding = self.model.get_text_features(**inputs)
            
            embedding = text_embedding.detach().cpu().numpy()[0]
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            
            return embedding
        except Exception as e:
            logger.error(f"Error encoding text '{text}': {e}")
            return None


class MultimodalRetriever:
    """Multimodal retrieval with text and image fusion."""
    
    def __init__(self, ml_loader: Any, products_df: Any, fusion_alpha: float = 0.7):
        """
        Initialize multimodal retriever.
        
        Args:
            ml_loader: MLLoader with indices
            products_df: Products DataFrame
            fusion_alpha: Fusion weight for text vs image (α=0.7 means 70% text, 30% image)
        """
        self.ml_loader = ml_loader
        self.products_df = products_df
        self.fusion_alpha = fusion_alpha
        self.image_processor = ImageQueryProcessor(ml_loader)
    
    def retrieve_by_text(self, query: str, k: int = 10) -> List[MultimodalResult]:
        """Retrieve products by text query."""
        try:
            results = self.ml_loader.search_text(query, k=k)
            
            multimodal_results = []
            for result in results:
                product = self.products_df[self.products_df['product_id'] == result.product_id]
                if not product.empty:
                    product_data = product.iloc[0]
                    multimodal_results.append(MultimodalResult(
                        product_id=result.product_id,
                        product_name=product_data.get('product_name', 'Unknown'),
                        category=product_data.get('category', 'Unknown'),
                        color=product_data.get('color', 'Unknown'),
                        text_score=float(result.score),
                        fused_score=float(result.score),
                        source="text"
                    ))
            
            return multimodal_results
        except Exception as e:
            logger.error(f"Error retrieving by text: {e}")
            return []
    
    def retrieve_by_image(self, image_path: str, k: int = 10) -> List[MultimodalResult]:
        """Retrieve products by image query."""
        try:
            # Encode image
            image_embedding = self.image_processor.encode_image(image_path)
            if image_embedding is None:
                return []
            
            # Search in image index
            distances, indices = self.ml_loader.image_index.search(
                np.array([image_embedding], dtype=np.float32), k=k
            )
            
            multimodal_results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx >= 0 and idx < len(self.products_df):
                    product = self.products_df.iloc[idx]
                    
                    # Convert distance to similarity (FAISS returns negated similarity)
                    similarity = float(distance)
                    
                    multimodal_results.append(MultimodalResult(
                        product_id=product['product_id'],
                        product_name=product.get('product_name', 'Unknown'),
                        category=product.get('category', 'Unknown'),
                        color=product.get('color', 'Unknown'),
                        image_score=similarity,
                        fused_score=similarity,
                        source="image"
                    ))
            
            return multimodal_results
        except Exception as e:
            logger.error(f"Error retrieving by image: {e}")
            return []
    
    def retrieve_multimodal(self, text_query: str = None, image_path: str = None,
                           k: int = 10) -> List[MultimodalResult]:
        """
        Retrieve products using multimodal fusion.
        
        Args:
            text_query: Text query (optional)
            image_path: Path to image query (optional)
            k: Number of results
        
        Returns:
            Fused multimodal results
        """
        start_time = time.time()
        
        results_text = []
        results_image = []
        
        # Get text results
        if text_query:
            results_text = self.retrieve_by_text(text_query, k=k)
        
        # Get image results
        if image_path:
            results_image = self.retrieve_by_image(image_path, k=k)
        
        # Fuse results
        fused = self._fuse_results(results_text, results_image, k=k)
        
        # Sort by fused score
        fused.sort(key=lambda x: x.fused_score, reverse=True)
        
        logger.info(f"Multimodal retrieval took {time.time() - start_time:.3f}s")
        
        return fused[:k]
    
    def _fuse_results(self, text_results: List[MultimodalResult],
                     image_results: List[MultimodalResult],
                     k: int = 10) -> List[MultimodalResult]:
        """Fuse text and image results using learned weights."""
        
        # Create score dictionary
        scores = {}
        
        # Add text scores
        for result in text_results:
            if result.product_id not in scores:
                scores[result.product_id] = {
                    "text": 0.0,
                    "image": 0.0,
                    "result": result
                }
            scores[result.product_id]["text"] = result.text_score
            scores[result.product_id]["result"] = result
        
        # Add image scores
        for result in image_results:
            if result.product_id not in scores:
                scores[result.product_id] = {
                    "text": 0.0,
                    "image": 0.0,
                    "result": result
                }
            scores[result.product_id]["image"] = result.image_score
            if result.product_id not in scores or result.text_score == 0:
                scores[result.product_id]["result"] = result
        
        # Compute fused scores
        fused_results = []
        for product_id, score_data in scores.items():
            text_score = score_data["text"]
            image_score = score_data["image"]
            
            # Fused score: α * text_score + (1-α) * image_score
            # α=0.7 means 70% weight to text, 30% to image
            fused_score = self.fusion_alpha * text_score + (1 - self.fusion_alpha) * image_score
            
            # Determine source
            has_text = text_score > 0
            has_image = image_score > 0
            if has_text and has_image:
                source = "both"
            elif has_text:
                source = "text"
            else:
                source = "image"
            
            # Update result
            result = score_data["result"]
            result.text_score = text_score
            result.image_score = image_score
            result.fused_score = fused_score
            result.source = source
            
            fused_results.append(result)
        
        return fused_results
    
    def get_multimodal_stats(self, results: List[MultimodalResult]) -> Dict:
        """Get statistics about multimodal results."""
        if not results:
            return {
                "total_results": 0,
                "text_only": 0,
                "image_only": 0,
                "multimodal": 0,
                "avg_text_score": 0,
                "avg_image_score": 0,
                "unique_products": 0
            }
        
        text_only = sum(1 for r in results if r.source == "text")
        image_only = sum(1 for r in results if r.source == "image")
        multimodal = sum(1 for r in results if r.source == "both")
        
        avg_text = np.mean([r.text_score for r in results if r.text_score > 0]) if any(r.text_score > 0 for r in results) else 0
        avg_image = np.mean([r.image_score for r in results if r.image_score > 0]) if any(r.image_score > 0 for r in results) else 0
        
        return {
            "total_results": len(results),
            "text_only": text_only,
            "image_only": image_only,
            "multimodal": multimodal,
            "avg_text_score": float(avg_text),
            "avg_image_score": float(avg_image),
            "unique_products": len(set(r.product_id for r in results))
        }
