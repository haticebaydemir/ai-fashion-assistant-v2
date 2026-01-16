"""ML Loader - Production Ready with 768d Embedding Support"""
import numpy as np
import pandas as pd
import faiss
import torch
from sentence_transformers import SentenceTransformer
from transformers import CLIPModel, CLIPProcessor
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class MLLoader:
    def __init__(self):
        """Initialize and load all ML models and indexes."""
        self.text_model = None
        self.clip_model = None
        self.clip_processor = None
        self.text_index = None
        self.image_index = None
        self.products_df = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._ready = False
        
        try:
            self._load_all()
            self._ready = True
        except Exception as e:
            logger.error(f"❌ ML Loader initialization failed: {e}", exc_info=True)
            raise
    
    def _load_all(self):
        """Load all ML components."""
        logger.info("🚀 Loading AI Fashion ML models...")
        
        # 1. Load sentence transformer for text (produces 768d)
        try:
            self.text_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
            logger.info("✅ Text model loaded (MPNet - 768d)")
        except Exception as e:
            logger.error(f"Failed to load text model: {e}")
            raise
        
        # 2. Load CLIP for images (produces 512d, will pad to 768d)
        try:
            self.clip_model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
            self.clip_processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
            self.clip_model.to(self.device)
            logger.info("✅ CLIP model loaded (ViT-B/32 - 512d → padded to 768d)")
        except Exception as e:
            logger.error(f"Failed to load CLIP model: {e}")
            raise
        
        # 3. Load product metadata
        data_path = Path("data/meta_ssot.csv")
        if not data_path.exists():
            raise FileNotFoundError(f"Product data not found: {data_path}")
        
        self.products_df = pd.read_csv(data_path)
        logger.info(f"✅ Products loaded: {len(self.products_df)}")
        
        # 4. Load text embeddings (768d from MPNet)
        embeddings_dir = Path("data/embeddings")
        mpnet_path = embeddings_dir / "mpnet_768d.npy"
        
        if not mpnet_path.exists():
            raise FileNotFoundError(f"Text embeddings not found: {mpnet_path}")
        
        text_emb = np.load(mpnet_path).astype('float32')
        
        # Normalize text embeddings
        norms = np.linalg.norm(text_emb, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        text_emb = text_emb / norms
        
        # Create FAISS index for text
        self.text_index = faiss.IndexFlatIP(text_emb.shape[1])
        self.text_index.add(text_emb)
        logger.info(f"✅ Text index: {self.text_index.ntotal} vectors (768d)")
        
        # 5. Load image embeddings (768d - padded from 512d CLIP)
        img_emb_path = embeddings_dir / "clip_image_768d_normalized.npy"
        
        if not img_emb_path.exists():
            logger.warning(f"⚠️ Image embeddings not found: {img_emb_path}")
            logger.warning("Image search will be disabled")
            self.image_index = None
        else:
            img_emb = np.load(img_emb_path).astype('float32')
            
            # Create FAISS index for images
            self.image_index = faiss.IndexFlatIP(img_emb.shape[1])
            self.image_index.add(img_emb)
            logger.info(f"✅ Image index: {self.image_index.ntotal} vectors (768d)")
        
        logger.info("🎉 ML Loader ready!")
    
    def is_ready(self):
        """Check if ML models are ready."""
        return self._ready
    
    def get_clip_dim(self):
        """Get CLIP model output dimension."""
        return 512  # ViT-B/32 outputs 512d
    
    def get_text_dim(self):
        """Get text model output dimension."""
        return 768  # MPNet outputs 768d
