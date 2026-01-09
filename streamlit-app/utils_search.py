"""
Search utilities for AI Fashion Assistant
v2.4.5 integration with Hugging Face Dataset support
"""

import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import streamlit as st
import os

@st.cache_resource
def load_models():
    """Load models (cached)"""
    
    # Load text encoder
    text_model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    return {
        'text_model': text_model
    }

@st.cache_data
def load_data():
    """Load product data and embeddings from Hugging Face Dataset"""
    
    try:
        from huggingface_hub import hf_hub_download
        
        # Download from Hugging Face Dataset
        embeddings_path = hf_hub_download(
            repo_id="HaticeB/fashion-assistant-data",
            filename="mpnet_768d.npy",
            repo_type="dataset",
            cache_dir=".cache"
        )
        
        products_path = hf_hub_download(
            repo_id="HaticeB/fashion-assistant-data",
            filename="meta_ssot.csv",
            repo_type="dataset",
            cache_dir=".cache"
        )
        
        # Load products
        products_df = pd.read_csv(products_path)
        
        # Load embeddings
        text_embeddings = np.load(embeddings_path)
        
        # Create FAISS index
        dimension = text_embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(text_embeddings.astype('float32'))
        
        return {
            'products': products_df,
            'index': index,
            'embeddings': text_embeddings
        }
    
    except ImportError:
        st.error("❌ huggingface-hub not installed. Add to requirements.txt")
        return None
    
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.info("💡 Make sure you've created the Hugging Face dataset with your data files")
        return None

def search_products(query: str, k: int = 10) -> List[Dict]:
    """
    Search for products using v2.4.5 multimodal system
    
    Args:
        query: Search query text
        k: Number of results to return
        
    Returns:
        List of product dictionaries with scores
    """
    
    # Load models and data
    models = load_models()
    data = load_data()
    
    if data is None:
        return []
    
    # Encode query
    text_model = models['text_model']
    query_embedding = text_model.encode([query])[0]
    query_embedding = query_embedding / np.linalg.norm(query_embedding)
    
    # Search
    index = data['index']
    scores, indices = index.search(
        query_embedding.reshape(1, -1).astype('float32'), 
        k
    )
    
    # Get results
    products_df = data['products']
    results = []
    
    for idx, score in zip(indices[0], scores[0]):
        product = products_df.iloc[idx]
        
        # Construct image path
        product_id = product['id']
        image_path = f"images/{product_id}.jpg"
        
        results.append({
            'id': int(product['id']),
            'name': product['productDisplayName'],
            'category': product['articleType'],
            'subcategory': product['subCategory'],
            'color': product['baseColour'],
            'gender': product['gender'],
            'season': product['season'],
            'usage': product['usage'],
            'score': float(score),
            'image_path': image_path
        })
    
    return results

def format_product_card(product: Dict) -> str:
    """Format product as HTML card"""
    
    return f"""
    <div style="
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: white;
    ">
        <h4 style="margin: 0 0 0.5rem 0;">{product['name']}</h4>
        <p style="margin: 0.25rem 0; color: #666;">
            <strong>Category:</strong> {product['category']} | 
            <strong>Color:</strong> {product['color']} | 
            <strong>Gender:</strong> {product['gender']}
        </p>
        <p style="margin: 0.25rem 0; color: #666;">
            <strong>Season:</strong> {product['season']} | 
            <strong>Usage:</strong> {product['usage']}
        </p>
        <p style="margin: 0.5rem 0; color: #1f77b4;">
            <strong>Relevance Score:</strong> {product['score']:.4f}
        </p>
    </div>
    """

def get_product_image(product_id: int) -> str:
    """Get product image path"""
    return f"images/{product_id}.jpg"
