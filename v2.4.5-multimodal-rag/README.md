# AI Fashion Assistant v2.4.5 - Multimodal RAG

**TÜBİTAK 2209-A Undergraduate Research Project**  
**Student:** Hatice Baydemir  
**Advisor:** İlya Kuş  
**Institution:** Karamanoğlu Mehmetbey University  

---

## 🎯 Project Overview

AI Fashion Assistant v2.4.5 is an advanced multimodal fashion search and recommendation system that combines:
- **Text search** using semantic embeddings
- **Image search** using CLIP visual features
- **Multimodal fusion** with learned weights
- **Visual-aware RAG** for intelligent responses

### Key Features

✅ **Image Query Support** - Search using product images  
✅ **Multimodal Fusion** - Combines text and visual signals (α=0.7)  
✅ **Visual Awareness** - 7.6 visual keywords per response  
✅ **Fast Response** - 0.64s average (28% faster than v2.2)  
✅ **Comprehensive Coverage** - 44,417 products indexed  

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Dataset Size** | 44,417 products |
| **Multimodal Unique** | 6.0 products avg |
| **Text-Image Overlap** | 0.4 products avg |
| **Response Time** | 0.642s avg |
| **Visual Keywords** | 7.6 per response |
| **Attribute Coverage** | 95.4% (42,388 products) |

---

## 🏗️ System Architecture

```
User Query (Text/Image)
        ↓
┌───────────────────────────────┐
│  Query Processing             │
│  - CLIP Text Encoding (768d)  │
│  - CLIP Image Encoding (768d) │
└───────────────────────────────┘
        ↓
┌───────────────────────────────┐
│  Multimodal Retrieval         │
│  - Text FAISS Index           │
│  - Image FAISS Index          │
│  - Learned Fusion (α=0.7)     │
└───────────────────────────────┘
        ↓
┌───────────────────────────────┐
│  Attribute Filtering          │
│  - V2.1 Visual Attributes     │
│  - Pattern/Style Matching     │
└───────────────────────────────┘
        ↓
┌───────────────────────────────┐
│  Visual-Aware RAG             │
│  - Context Building           │
│  - Visual Attribute Prompts   │
│  - GROQ Llama-3.3-70B         │
└───────────────────────────────┘
        ↓
   Response to User
```

---

## 📁 Repository Structure

```
ai_fashion_assistant_v2/
├── data/
│   ├── processed/
│   │   └── meta_ssot.csv              # 44,417 products
│   └── raw/
│       └── images/                     # Product images
├── v2.0-baseline/
│   ├── embeddings/
│   │   ├── text/mpnet_768d.npy        # MPNet embeddings
│   │   └── image/clip_image_768d.npy  # CLIP image embeddings
│   └── notebooks/                      # 30+ notebooks
├── v2.1-core-ml-plus/
│   └── evaluation/results/
│       └── product_attributes.csv      # 307K visual attributes
├── v2.2-rag/
│   └── notebooks/                      # RAG implementation
├── v2.4-personalization/
│   └── notebooks/                      # User personalization
├── v2.4.5-multimodal-rag/
│   ├── notebooks/
│   │   ├── 01_multimodal_rag_architecture.ipynb
│   │   ├── 02_image_query_processing.ipynb
│   │   ├── 03_multimodal_retrieval.ipynb
│   │   ├── 04_visual_aware_rag.ipynb
│   │   ├── 05_evaluation_metrics.ipynb
│   │   └── 06_final_documentation.ipynb
│   └── evaluation/results/
│       ├── retrieval_comparison.json
│       ├── visual_rag_responses.json
│       ├── performance_report.md
│       ├── performance_visualization.png
│       └── v2.4.5_comprehensive_results.xlsx
└── README.md
```

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install dependencies
pip install numpy pandas torch transformers
pip install faiss-cpu sentence-transformers
pip install groq pillow opencv-python
```

### 2. Load Models

```python
from transformers import CLIPModel, CLIPProcessor

# Load CLIP
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
```

### 3. Run Multimodal Search

```python
# Text query
results_text = retriever.retrieve_by_text("white shirts", k=10)

# Image query
results_image = retriever.retrieve_by_image("path/to/image.jpg", k=10)

# Multimodal fusion
results_multimodal = retriever.retrieve_multimodal(
    text_query="white shirts",
    image_path="path/to/image.jpg",
    k=10
)
```

---

## 📈 Version History

### v2.0 - Text-Only Baseline (Completed)
- MPNet text embeddings
- FAISS HNSW indexing
- NDCG@10: 0.974

### v2.1 - Core ML+ (Completed)
- CLIP visual features
- 307K visual attributes extracted
- Learned fusion weights

### v2.2 - RAG System (Completed)
- GROQ Llama-3.3-70B
- Context-aware responses
- RAG Score: 0.714

### v2.4 - Personalization (Completed)
- User profile management
- Content-based filtering
- 76.7% preference match

### v2.4.5 - Multimodal RAG (Current)
- Image query support
- Multimodal fusion retrieval
- Visual-aware RAG responses
- 7.6 visual keywords per response

---

## 📊 Evaluation Results

### Retrieval Performance
- Text-only: 10 results per query
- Image-only: 10 results per query
- Multimodal: 10 fused results
- Unique products via fusion: 6.0 avg

### RAG Quality
- Response time: 0.642s avg (0.581s - 0.727s)
- Response length: ~496 characters
- Visual awareness: 7.6 keywords per response
- Improvement vs v2.2: 28% faster, 100% more visual

---

## 🎓 Academic Contribution

### Novel Aspects
1. **Multimodal Fashion Search** - First implementation combining CLIP text/image for Turkish fashion dataset
2. **Learned Fusion Strategy** - Empirically derived α=0.7 weight
3. **Visual-Aware RAG** - Integration of visual attributes in LLM prompts
4. **Production-Ready System** - Sub-second response time at scale

### Technical Innovations
- CLIP text embeddings for all 44K products (vs MPNet baseline)
- V2.1 attribute integration (307K visual features)
- Attribute-based post-filtering
- Visual reasoning in natural language responses

---

## 👥 Team

**Student Researcher:** Hatice Baydemir  
**Advisor:** İlya Kuş  
**Institution:** Karamanoğlu Mehmetbey University  
**Department:** Computer Engineering  
**Program:** TÜBİTAK 2209-A Undergraduate Research  

---

**Last Updated:** January 2026  
**Version:** 2.4.5  
**Status:** ✅ Complete - Ready for User Study
