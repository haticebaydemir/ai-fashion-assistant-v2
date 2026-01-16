"""Fashion Search Engine - Production Ready with 768d Support"""
import numpy as np
import torch
from typing import List, Optional
from PIL import Image
from dataclasses import dataclass
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    rank: int
    product_id: int
    product_name: str
    category: str
    gender: str
    color: str
    score: float
    image_url: Optional[str] = None

class FashionSearchEngine:
    def __init__(self, ml_loader=None):
        """Initialize search engine with ML loader."""
        self.ml = ml_loader
        if self.ml is None:
            try:
                from app.core.ml_loader import MLLoader
                self.ml = MLLoader()
                logger.info("✅ ML Loader initialized via lazy loading")
            except Exception as e:
                logger.error(f"❌ ML Loader failed: {e}")
                self.ml = None
    
    def _check_ml_loaded(self):
        """Check if ML models are loaded."""
        if self.ml is None:
            raise RuntimeError(
                "ML models not loaded. Please ensure:\n"
                "1. data/embeddings/mpnet_768d.npy exists (~200 MB)\n"
                "2. data/embeddings/clip_image_768d_normalized.npy exists (~500 MB)\n"
                "3. data/meta_ssot.csv exists"
            )
    
    def encode_text(self, text: str) -> np.ndarray:
        """Encode text query using MPNet (768d)."""
        self._check_ml_loaded()
        emb = self.ml.text_model.encode([text], convert_to_numpy=True)[0]
        return (emb / np.linalg.norm(emb)).astype('float32')
    
    def encode_image(self, image: Image.Image) -> np.ndarray:
        """
        Encode image using CLIP and pad to 768d.
        
        CLIP ViT-B/32 produces 512d embeddings.
        Our index expects 768d, so we pad with zeros.
        """
        self._check_ml_loaded()
        
        # CLIP preprocessing and encoding
        inputs = self.ml.clip_processor(images=image, return_tensors="pt")
        inputs = {k: v.to(self.ml.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            emb = self.ml.clip_model.get_image_features(**inputs).cpu().numpy()[0]
        
        # Normalize
        emb = emb / np.linalg.norm(emb)
        
        # ✅ CRITICAL: Pad 512d → 768d to match index dimension
        if emb.shape[0] == 512:
            padding = np.zeros(256, dtype=np.float32)
            emb = np.concatenate([emb, padding])
            logger.debug("Padded CLIP embedding from 512d to 768d")
        
        return emb.astype('float32')
    
    def search(self, text=None, image=None, k=10, alpha=0.7) -> List[SearchResult]:
        """
        Search for products using text and/or image queries.
        
        Args:
            text: Text query
            image: PIL Image
            k: Number of results
            alpha: Weight for text vs image (0-1, only for multimodal)
            
        Returns:
            List of SearchResult objects
        """
        # Validate inputs
        if self.ml is None:
            raise RuntimeError("ML models not loaded")
        
        if not text and not image:
            raise ValueError("Either text or image query must be provided")
        
        # Multimodal search (text + image)
        if text and image:
            if not self.ml.text_index or not self.ml.image_index:
                raise RuntimeError("Both text and image indexes required for multimodal search")
            
            # Text search
            text_emb = self.encode_text(text)
            t_k = min(k * 3, max(1, self.ml.text_index.ntotal))
            text_scores, text_indices = self.ml.text_index.search(
                text_emb.reshape(1, -1), t_k
            )
            text_scores = np.clip((text_scores[0] + 1.0) / 2.0, 0, 1)
            text_indices = text_indices[0]
            
            # Image search
            image_emb = self.encode_image(image)
            i_k = min(k * 3, max(1, self.ml.image_index.ntotal))
            img_scores, img_indices = self.ml.image_index.search(
                image_emb.reshape(1, -1), i_k
            )
            img_scores = np.clip((img_scores[0] + 1.0) / 2.0, 0, 1)
            img_indices = img_indices[0]
            
            # Fusion
            combined = {}
            for idx, score in zip(text_indices, text_scores):
                combined[int(idx)] = score * alpha
            for idx, score in zip(img_indices, img_scores):
                combined[int(idx)] = combined.get(int(idx), 0.0) + score * (1 - alpha)
            
            sorted_items = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:k]
            indices = [idx for idx, _ in sorted_items]
            scores = [score for _, score in sorted_items]
        
        # Text-only search
        elif text:
            if not self.ml.text_index:
                raise RuntimeError("Text index not loaded")
            
            emb = self.encode_text(text)
            scores_arr, indices_arr = self.ml.text_index.search(emb.reshape(1, -1), k)
            scores = np.clip((scores_arr[0] + 1.0) / 2.0, 0, 1)
            indices = indices_arr[0]
        
        # Image-only search
        elif image:
            if not self.ml.image_index:
                raise RuntimeError("Image index not loaded")
            
            emb = self.encode_image(image)
            scores_arr, indices_arr = self.ml.image_index.search(emb.reshape(1, -1), k)
            scores = np.clip((scores_arr[0] + 1.0) / 2.0, 0, 1)
            indices = indices_arr[0]
        
        # Format results
        # Format results
        results = []
        for rank, (idx, score) in enumerate(zip(indices, scores), 1):
            if idx < 0 or idx >= len(self.ml.products_df):
                continue
            
            p = self.ml.products_df.iloc[idx]
            
            # Build image URL
            image_url = None
            local_img = Path("data/images") / f"{int(p['id'])}.jpg"
            if local_img.exists():
                image_url = f"http://localhost:8000/images/{int(p['id'])}.jpg"
            elif 'image_path' in p and str(p['image_path']).startswith('http'):
                image_url = p['image_path']
            
            results.append(SearchResult(
                rank=rank,
                product_id=int(p['id']),
                product_name=p['productDisplayName'],
                category=p.get('masterCategory', 'Unknown'),
                gender=p.get('gender', 'Unknown'),
                color=p.get('baseColour', 'Unknown'),
                score=float(score),
                image_url=image_url
            ))

        return results
            
