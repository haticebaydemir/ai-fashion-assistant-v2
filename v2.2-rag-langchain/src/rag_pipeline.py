"""
Fashion RAG Pipeline - Production Implementation
AI Fashion Assistant v2.2

Author: Hatice Baydemir
Date: January 2, 2026
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import faiss
from groq import Groq
from pathlib import Path
import json
from datetime import datetime


class FashionRAGPipeline:
    """
    Production-ready RAG pipeline for fashion product search.
    
    Features:
    - FAISS vector search (44K products)
    - GROQ LLM integration (Llama-3.3-70B)
    - Response caching for efficiency
    - Batch processing support
    - Configurable retrieval parameters
    
    Example:
        >>> pipeline = FashionRAGPipeline(
        ...     metadata_path="data/processed/meta_ssot.csv",
        ...     embeddings_path="v2.0-baseline/embeddings/text/mpnet_768d.npy",
        ...     groq_api_key="your_key"
        ... )
        >>> result = pipeline.query("blue summer dress")
        >>> print(result['answer'])
    """
    
    def __init__(
        self,
        metadata_path: str,
        embeddings_path: str,
        groq_api_key: str,
        encoder_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        llm_model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.1,
        max_tokens: int = 500
    ):
        """
        Initialize the RAG pipeline.
        
        Args:
            metadata_path: Path to product metadata CSV
            embeddings_path: Path to precomputed embeddings
            groq_api_key: GROQ API key
            encoder_model: Sentence transformer model name
            llm_model: GROQ LLM model name
            temperature: LLM temperature (0-1)
            max_tokens: Max tokens for LLM response
        """
        print("Initializing FashionRAGPipeline...")
        
        # Store config
        self.config = {
            'encoder_model': encoder_model,
            'llm_model': llm_model,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        
        # Load data
        self.metadata = pd.read_csv(metadata_path)
        self.embeddings = np.load(embeddings_path)
        
        # Normalize embeddings for cosine similarity
        self.embeddings_norm = self.embeddings / np.linalg.norm(
            self.embeddings, axis=1, keepdims=True
        )
        
        # Setup encoder
        self.encoder = SentenceTransformer(encoder_model)
        
        # Build FAISS index
        dimension = self.embeddings_norm.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(self.embeddings_norm.astype('float32'))
        
        # Setup LLM client
        self.llm_client = Groq(api_key=groq_api_key)
        
        # Create product documents
        self.product_docs = self._create_documents()
        
        # Initialize cache
        self.cache = {}
        self.stats = {'queries': 0, 'cache_hits': 0}
        
        print(f"✅ Pipeline ready!")
        print(f"   Products: {len(self.metadata):,}")
        print(f"   Index: {self.index.ntotal:,} vectors ({dimension}d)")
    
    def _create_documents(self) -> List[str]:
        """Create text documents from product metadata."""
        docs = []
        for _, row in self.metadata.iterrows():
            doc = f"""{row['productDisplayName']}. 
Category: {row.get('masterCategory', 'Unknown')}. 
Type: {row.get('articleType', 'Unknown')}. 
Color: {row.get('baseColour', 'Unknown')}. 
Gender: {row.get('gender', 'Unisex')}. 
Season: {row.get('season', 'All')}."""
            docs.append(doc)
        return docs
    
    def retrieve(self, query: str, k: int = 5) -> Dict:
        """
        Retrieve relevant products using vector search.
        
        Args:
            query: Natural language query
            k: Number of products to retrieve
            
        Returns:
            Dict with indices, scores, products
        """
        # Encode query
        query_emb = self.encoder.encode([query])[0]
        query_emb = query_emb / np.linalg.norm(query_emb)
        
        # Search FAISS
        scores, indices = self.index.search(
            query_emb.reshape(1, -1).astype('float32'),
            k
        )
        
        return {
            'indices': indices[0].tolist(),
            'scores': scores[0].tolist(),
            'products': [self.product_docs[i] for i in indices[0]]
        }
    
    def augment(self, query: str, retrieved: Dict) -> str:
        """
        Create augmented prompt with retrieved context.
        
        Args:
            query: User query
            retrieved: Retrieved products dict
            
        Returns:
            Augmented prompt string
        """
        context = "\n\n".join([
            f"{i+1}. {prod}" 
            for i, prod in enumerate(retrieved['products'])
        ])
        
        prompt = f"""You are a fashion shopping assistant. Recommend products based on the user's query.

Available Products:
{context}

User Query: {query}

Recommendation (be specific, mention product names):"""
        
        return prompt
    
    def generate(self, prompt: str) -> str:
        """
        Generate answer using LLM.
        
        Args:
            prompt: Augmented prompt
            
        Returns:
            Generated answer
        """
        response = self.llm_client.chat.completions.create(
            model=self.config['llm_model'],
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config['temperature'],
            max_tokens=self.config['max_tokens']
        )
        return response.choices[0].message.content
    
    def query(self, query: str, k: int = 5, use_cache: bool = True) -> Dict:
        """
        Complete RAG query pipeline.
        
        Args:
            query: Natural language query
            k: Number of products to retrieve
            use_cache: Whether to use cached responses
            
        Returns:
            Dict with query, answer, retrieved products, scores
        """
        self.stats['queries'] += 1
        
        # Check cache
        cache_key = f"{query}_{k}"
        if use_cache and cache_key in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[cache_key]
        
        # RAG pipeline: Retrieve → Augment → Generate
        retrieved = self.retrieve(query, k)
        prompt = self.augment(query, retrieved)
        answer = self.generate(prompt)
        
        result = {
            'query': query,
            'answer': answer,
            'retrieved_products': retrieved['products'],
            'scores': retrieved['scores'],
            'indices': retrieved['indices'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Cache result
        if use_cache:
            self.cache[cache_key] = result
        
        return result
    
    def batch_query(self, queries: List[str], k: int = 5) -> List[Dict]:
        """
        Process multiple queries in batch.
        
        Args:
            queries: List of queries
            k: Number of products per query
            
        Returns:
            List of results
        """
        return [self.query(q, k) for q in queries]
    
    def get_stats(self) -> Dict:
        """Get pipeline statistics."""
        cache_hit_rate = (
            self.stats['cache_hits'] / self.stats['queries'] 
            if self.stats['queries'] > 0 else 0
        )
        return {
            **self.stats,
            'cache_hit_rate': cache_hit_rate,
            'cache_size': len(self.cache)
        }
    
    def save_cache(self, path: str):
        """Save cache to JSON file."""
        with open(path, 'w') as f:
            json.dump(self.cache, f, indent=2)
        print(f"✅ Cache saved: {len(self.cache)} entries")
    
    def load_cache(self, path: str):
        """Load cache from JSON file."""
        with open(path, 'r') as f:
            self.cache = json.load(f)
        print(f"✅ Cache loaded: {len(self.cache)} entries")


if __name__ == "__main__":
    # Example usage
    pipeline = FashionRAGPipeline(
        metadata_path="data/processed/meta_ssot.csv",
        embeddings_path="v2.0-baseline/embeddings/text/mpnet_768d.npy",
        groq_api_key="YOUR_KEY_HERE"
    )
    
    # Single query
    result = pipeline.query("blue summer dress")
    print(result['answer'])
    
    # Batch queries
    queries = ["red lipstick", "black shoes", "winter jacket"]
    results = pipeline.batch_query(queries)
