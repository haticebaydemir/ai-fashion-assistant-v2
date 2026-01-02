# 🛍️ AI Fashion Assistant v2.0 → v2.5

**A production-ready multimodal fashion search system with GenAI enhancements, achieving 97.4% NDCG@10 through learned fusion and comprehensive visual attribute extraction**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![TÜBİTAK](https://img.shields.io/badge/TÜBİTAK-2209--A-red.svg)](https://www.tubitak.gov.tr/)
[![Dataset](https://img.shields.io/badge/Dataset-Kaggle-20BEFF.svg)](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Overview

This repository contains a complete implementation of a multimodal fashion product search system developed as part of the TÜBİTAK 2209-A Undergraduate Research Program. The system processes 44,417 fashion products using state-of-the-art transformer models (CLIP, sentence-transformers) and achieves near-perfect ranking performance through learned fusion strategies.

**Research Highlights:**
- 🎯 **97.4% NDCG@10** - State-of-the-art ranking performance
- ⚡ **100% MRR** - Perfect first-rank accuracy across test queries
- 🔍 **51.1% Recall@10** - Effective retrieval from large catalog
- 📊 **104 diverse test queries** - Comprehensive bilingual evaluation (v2.1+)
- 🎨 **307K visual attributes** - CLIP zero-shot extraction (v2.1+)
- 🚀 **Production-ready** - Complete deployment pipeline included

---

## 🗺️ Development Roadmap

This project follows a structured 7-week development roadmap (January 2 - February 19, 2026):

### ✅ v2.0: Stable Baseline (September-December 2025)
- Core multimodal search system
- 97.4% NDCG@10 baseline performance
- Production deployment pipeline
- 30+ research notebooks

### ✅ v2.1: Core ML + Visual Attributes (Week 1-2, January 1-2, 2026)
- **Status:** COMPLETE
- Learned fusion optimization (α=0.7)
- Visual attribute extraction (307K attributes, 10 categories)
- Explainability system (fusion decomposition)
- Comprehensive query generation (104 bilingual queries)
- Baseline comparisons (7 methods, RRF evaluation)
- **[See v2.1-core-ml-plus/README.md](./v2.1-core-ml-plus/README.md)**

### ✅ v2.2: RAG Pipeline (Week 3, January 3, 2026)
- **Status:** COMPLETE
- Production-ready RAG (Retrieval-Augmented Generation)
- 3 professional notebooks (fundamentals, production, evaluation)
- FashionRAGPipeline class with caching & batch processing
- Comprehensive evaluation (30 queries, 0.714 avg score, 0.89s response time)
- Framework-agnostic implementation (no LangChain dependency)
- **[See v2.2-rag-langchain/README.md](./v2.2-rag-langchain/README.md)**

### 📅 v2.3: AI Agents (Week 4-5)
- Conversational AI agents
- Multi-turn dialogue management
- Tool-using capabilities
- **Status:** Planned

### 📅 v2.4: User Study + Paper (Week 6-7)
- User study (20-25 participants)
- Academic paper finalization
- Production deployment
- **Status:** Planned

---

## 🏗️ System Architecture

The system implements a four-stage pipeline optimized for fashion e-commerce:
```
┌─────────────────────────────────────────────────┐
│         1. Query Processing                     │
│    Intent Detection • Slot Extraction           │
│    Multi-language Support (TR/EN)               │
│    LLM-based Query Expansion (v2.1+)            │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│      2. Multimodal Embedding                    │
│    Text: mpnet (768d) + CLIP text (512d)       │
│    Image: CLIP vision (768d)                    │
│    Visual Attributes: 10 categories (v2.1+)     │
│    Combined Space: 1280-dimensional             │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│         3. Vector Retrieval (FAISS)             │
│    IndexFlatIP • Cosine Similarity              │
│    44,417 products • <10ms latency              │
│    Learned Fusion: α=0.7 (v2.1+)               │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│      4. Learned Ranking & Explainability        │
│    Feature Fusion • Attribute Awareness         │
│    Personalization • Reranking                  │
│    Natural Language Explanations (v2.1+)        │
└─────────────────────────────────────────────────┘
```

---

## 📂 Repository Structure

This repository is organized into versioned directories for maintainability and reproducibility:

### 🔒 [v2.0-baseline/](./v2.0-baseline/) - Stable Research Baseline

**Status:** Frozen • Complete • Production-Ready

The baseline contains all completed research from September-December 2024:
```
v2.0-baseline/
├── research/                    # 30+ Jupyter notebooks
│   ├── notebooks/               # Phase 0-10 development
│   │   ├── phase0_setup/
│   │   ├── phase1_foundation/
│   │   ├── phase2_embeddings/
│   │   ├── phase3_retrieval/
│   │   ├── phase4_evaluation/
│   │   ├── phase5_optimization/
│   │   ├── phase6_advanced_features/
│   │   ├── phase7_api_deployment/
│   │   ├── phase8_llm_features/
│   │   ├── phase9_evaluation/
│   │   └── phase10_reproducibility/
│   ├── experiments/             # Experimental runs
│   └── llm/                     # LLM feature experiments
│
├── src/                         # Production code
│   ├── schema.py                # SSOT data schemas
│   ├── search_engine.py         # Core search implementation
│   └── config.py                # Configuration management
│
├── models/                      # Trained models
│   ├── advanced_ranker.pkl      # LightGBM fusion ranker
│   ├── fusion_ranker.pkl
│   ├── query_expander.pkl
│   └── personalization/         # ALS collaborative filtering
│
├── data/                        # Processed datasets & schemas
├── embeddings/                  # Precomputed vectors (44,417 products)
├── evaluation/                  # Benchmark results & comparisons
│
├── deployment/                  # Production deployment
│   ├── E_Ticaret_Chatbot_DEMO.ipynb  # Live demo
│   ├── DEPLOYMENT.md            # Deployment guide
│   ├── api/                     # FastAPI backend
│   ├── ui/                      # Streamlit frontend
│   ├── docker/                  # Docker configs
│   └── monitoring/              # Prometheus + Grafana
│
├── docs/                        # Documentation
│   ├── evaluation/              # Performance reports
│   ├── TUBITAK_ROADMAP.md
│   └── REPRODUCIBILITY.md
│
├── paper/                       # Academic paper materials
├── schemas/                     # Schema definitions
├── visual_search/               # Visual search experiments
└── README.md                    # Detailed documentation
```

**📖 [See v2.0-baseline/README.md for complete documentation](./v2.0-baseline/README.md)**

---

### ✅ [v2.1-core-ml-plus/](./v2.1-core-ml-plus/) - GenAI Enhancements

**Status:** Complete (January 1-2, 2025)

Core machine learning improvements and visual attribute extraction:
```
v2.1-core-ml-plus/
├── notebooks/
│   ├── 01_visual_attributes_extraction.ipynb
│   ├── 02_explainability_and_query_generation.ipynb
│   └── 03_baseline_comparisons.ipynb
│
├── models/
│   └── fusion_model_initial.pth
│
├── evaluation/
│   ├── queries.txt
│   └── results/
│       ├── product_attributes.csv           # 307K attributes
│       ├── enhanced_products.csv            # Products + attributes
│       ├── evaluation_queries_100plus.csv   # 104 test queries
│       ├── baseline_comparison_RRF.csv      # Method comparison
│       └── category_performance.csv         # Category analysis
│
└── README.md
```

**Key Features:**
- ✅ Learned fusion model (α=0.7 optimal weighting)
- ✅ CLIP zero-shot visual attributes (10 categories, 307K total)
- ✅ Explainability system (fusion score decomposition)
- ✅ LLM-based query generation (104 bilingual queries via GROQ)
- ✅ Comprehensive baseline evaluation (7 methods, RRF consensus)

**📖 [See v2.1-core-ml-plus/README.md for detailed documentation](./v2.1-core-ml-plus/README.md)**

---

### ✅ [v2.2-rag-langchain/](./v2.2-rag-langchain/) - RAG Pipeline

**Status:** Complete (January 3, 2026)

Production-ready RAG (Retrieval-Augmented Generation) implementation:
```
v2.2-rag-langchain/
├── notebooks/
│   ├── 01_rag_fundamentals.ipynb      # RAG from scratch (21 cells)
│   ├── 02_production_pipeline.ipynb   # Production class (18 cells)
│   └── 03_evaluation.ipynb            # Comprehensive eval (23 cells)
│
├── src/
│   └── rag_pipeline.py                # FashionRAGPipeline class
│
├── evaluation/
│   └── results/
│       ├── evaluation_results.csv     # 30 query results
│       ├── evaluation_stats.json      # Performance stats
│       ├── category_performance.csv   # Category breakdown
│       └── score_distribution.png     # Visualization
│
├── configs/
│   └── pipeline_config.json           # Configuration
│
├── cache.json                         # Response cache
└── README.md                          # Complete documentation
```

**Key Features:**
- ✅ Production `FashionRAGPipeline` class (retrieve → augment → generate)
- ✅ GROQ LLM integration (Llama-3.3-70B, 0.89s avg response time)
- ✅ FAISS vector search (44,417 products, <100ms retrieval)
- ✅ Response caching & batch processing
- ✅ 30-query evaluation (0.714 avg score across 3 categories)
- ✅ Framework-agnostic (4 core dependencies, no LangChain)

**Performance:**
- Average retrieval score: 0.714
- Response time: 0.89s
- Best category: Simple items (0.758)
- Cache hit rate: Configurable

**📖 [See v2.2-rag-langchain/README.md for detailed documentation](./v2.2-rag-langchain/README.md)**

---

## 📊 Dataset

**Source:** [Fashion Product Images Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)

**Kaggle Dataset by Param Aggarwal**

| Statistic | Value |
|-----------|-------|
| Total Products | 44,417 |
| Master Categories | 7 (Apparel, Accessories, Footwear, etc.) |
| Sub-categories | 45 |
| Unique Colors | 46 |
| Attributes | 8 (gender, category, color, season, usage, year, articleType, baseColour) |
| **Visual Attributes (v2.1+)** | **10 categories, 307K total** |
| Image Resolution | 80×60 to 2400×3200 pixels |
| File Format | JPG images + CSV metadata |
| Total Size | ~4.5 GB |

---

## 🎯 Performance Metrics

### v2.0 Baseline (December 2024)

Evaluated on **22 diverse test queries** covering specific items, general categories, and attribute-based searches.

| Metric | Baseline | Fusion | Improvement |
|--------|----------|--------|-------------|
| **NDCG@10** | 97.30% | **97.43%** | +0.13pp |
| **NDCG@5** | 97.61% | 97.61% | - |
| **Recall@10** | 50.61% | **51.11%** | +0.50pp |
| **Recall@5** | 25.36% | 25.36% | - |
| **Precision@10** | 97.73% | 97.73% | - |
| **Precision@5** | 98.18% | 98.21% | +0.03pp |
| **MRR** | 100% | 100% | Perfect first-rank |

### v2.1 Enhancements (January 2025)

**Visual Attributes:**
- 307,720 attributes extracted
- 6.93 avg attributes per product
- 95.4% product coverage
- 10 semantic categories (pattern, fit, length, neckline, sleeve, material, formality, season, occasion, style)

**Baseline Comparison (104 queries, 7 methods):**
- **Best Method:** Fusion α=0.7 (our method)
- **Consensus Overlap@10:** 0.6779
- **Rank Correlation:** 0.8833
- Multimodal fusion outperforms all unimodal baselines

**Query Generation:**
- 104 bilingual queries (59 English, 45 Turkish)
- 7 categories (simple, attribute, occasion, style, complex, seasonal, budget)
- Generated via GROQ Llama-3.3-70B with validation

---

## 🔬 Technical Implementation

### Embedding Models

**Text Encoding:**
- **Primary:** `paraphrase-multilingual-mpnet-base-v2` (768d)
  - Multilingual semantic understanding (Turkish + English)
  - Trained on 1B+ sentence pairs
- **Secondary:** OpenAI CLIP text encoder (512d)
  - Multimodal text-image alignment
- **Combined:** Concatenated 1280-dimensional space

**Image Encoding:**
- **Model:** OpenAI CLIP ViT-Large/14 (768d) - upgraded in v2.1
- **Preprocessing:** Center crop, normalize to ImageNet statistics
- **Zero-shot Attributes:** 10 semantic categories via CLIP classification (v2.1+)

**Fusion Strategy (v2.1+):**
- **Learned weighting:** α=0.7 (70% text, 30% image)
- **Rationale:** Fashion queries are primarily descriptive
- **Optimization:** Empirically validated on 104 diverse queries

### Search Infrastructure

**Vector Index:**
- **Type:** FAISS IndexFlatIP (inner product / cosine similarity)
- **Size:** 44,417 product embeddings
- **Latency:** <10ms retrieval (p95)
- **Storage:** Optimized for memory-mapped files

**Ranking Pipeline:**
1. **Baseline Retrieval:** Direct cosine similarity (NDCG@10: 97.30%)
2. **Learned Fusion:** Optimized α=0.7 weighting (v2.1)
3. **Advanced Ranking:** LightGBM ranker with features:
   - Text similarity score
   - Image similarity score
   - Attribute match indicators
   - Historical popularity
   - **Result:** NDCG@10: 97.43%
4. **Personalization (Optional):** ALS collaborative filtering with 64d user embeddings

**Explainability (v2.1+):**
- Fusion score decomposition (text vs image contribution)
- Attribute-based matching explanations
- Natural language generation for search results

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.10+
CUDA GPU (optional, for faster inference)
16GB+ RAM
```

### Installation
```bash
# Clone repository
git clone https://github.com/haticebaydemir/ai-fashion-assistant-v2.git
cd ai-fashion-assistant-v2

# Install dependencies
pip install -r requirements.txt
```

### Running the Demo

**Option 1: Local Jupyter Notebooks**
```bash
jupyter notebook
# Navigate to v2.0-baseline/research/notebooks/phase10_reproducibility/
# Or v2.1-core-ml-plus/notebooks/ for latest features
```

**Option 2: Google Colab Demo**
1. Open [`v2.0-baseline/deployment/E_Ticaret_Chatbot_DEMO.ipynb`](./v2.0-baseline/deployment/E_Ticaret_Chatbot_DEMO.ipynb) in Colab
2. Follow setup instructions in [`DEPLOYMENT.md`](./v2.0-baseline/deployment/DEPLOYMENT.md)
3. Run cells sequentially
4. Access via ngrok public URL

---

## 🛠️ Technology Stack

### Core Dependencies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Text Embeddings** | sentence-transformers | 2.2.2 | Semantic text encoding |
| **Multimodal** | transformers (CLIP) | 4.30.2 | Vision-language models |
| **Deep Learning** | PyTorch | 2.0.1 | Model inference |
| **Vector Search** | FAISS | 1.7.2 | Similarity search |
| **Ranking** | LightGBM | 4.0.0 | Gradient boosting |
| **Personalization** | implicit | 0.7.2 | Collaborative filtering (ALS) |
| **LLM (v2.1+)** | GROQ | 0.4.0 | Query generation |
| **Backend API** | FastAPI | 0.109.0 | REST API server |
| **Frontend** | Streamlit | 1.28.0 | Web interface |
| **Deployment** | Docker | 24.0+ | Containerization |
| **Monitoring** | Prometheus + Grafana | - | Metrics & dashboards |

### Development Tools
```bash
# Data processing
pandas==2.0.3
numpy==1.24.3
Pillow==10.0.0

# API & Web
uvicorn[standard]==0.27.0
python-multipart==0.0.6
pyngrok==7.0.0

# Utilities
pydantic==2.5.3
PyYAML==6.0
```

---

## 📚 Development Phases

### v2.0 Research (September-December 2025)

The project was developed in 10 phases over 4 months:

| Phase | Focus | Key Outputs | Status |
|-------|-------|-------------|--------|
| **0-1** | Foundation & SSOT | Data schemas, preprocessing pipeline | ✅ Complete |
| **2** | Embeddings | Model selection, 44,417 embeddings generated | ✅ Complete |
| **3** | Retrieval | FAISS index, baseline search (NDCG: 97.30%) | ✅ Complete |
| **4** | Evaluation | Metrics framework, 22 test queries | ✅ Complete |
| **5** | Optimization | LightGBM ranker (NDCG: 97.43%) | ✅ Complete |
| **6** | Personalization | ALS collaborative filtering | ✅ Complete |
| **7** | Deployment | FastAPI, Docker, monitoring | ✅ Complete |
| **8** | LLM Features | Query rewriting, dialogue (experimental) | ✅ Complete |
| **9** | Final Evaluation | Comprehensive benchmarks | ✅ Complete |
| **10** | Reproducibility | Documentation, validation | ✅ Complete |

### v2.1+ GenAI Enhancements (January-February 2026)

| Version | Focus | Timeline | Status |
|---------|-------|----------|--------|
| **v2.1** | Core ML + Visual Attributes | Week 1-2 (Jan 1-2) | ✅ Complete |
| **v2.2** | RAG + LangChain | Week 3-4 | 🔄 In Development |
| **v2.3** | AI Agents | Week 5 | 📅 Planned |
| **v2.4** | User Study + Paper | Week 6-7 | 📅 Planned |

**📖 Detailed phase documentation:** See [`v2.0-baseline/research/notebooks/`](./v2.0-baseline/research/notebooks/) and version-specific READMEs.

---

## 🎓 Academic Context

### Research Program

**Program:** TÜBİTAK 2209-A Undergraduate Research Projects Support Program

**Duration:** September 2025 - February 2026

**Student Researcher:** Hatice Baydemir

**Advisor:** İlya Kuş

**Institution:** Karamanoğlu Mehmetbey University

### Key Contributions

1. **Novel Multimodal Fusion Strategy**
   - Learned fusion of semantic (mpnet) and visual (CLIP) embeddings
   - Achieves 97.4% NDCG@10 on fashion product search
   - Outperforms text-only and image-only baselines
   - Optimized weighting (α=0.7) validates descriptive nature of fashion queries

2. **Visual Attribute Extraction (v2.1)**
   - 307K attributes extracted via CLIP zero-shot classification
   - 10 semantic categories with 95.4% product coverage
   - Enables fine-grained attribute-aware search

3. **Comprehensive Evaluation Framework**
   - Rigorous evaluation on 104 diverse bilingual queries
   - 7 baseline method comparisons with RRF consensus ground truth
   - Query type analysis (simple, attribute, occasion, style, complex, seasonal, budget)
   - Category-wise performance breakdown

4. **Production-Ready Implementation**
   - Complete end-to-end pipeline from raw data to deployment
   - SSOT (Single Source of Truth) framework for reproducibility
   - 30+ documented notebooks covering all development phases
   - Explainability system for transparent search results

5. **Open Source Release**
   - Fully documented codebase with reproducibility guides
   - Clean separation of research and production code
   - Deployment configs for Docker and cloud platforms
   - Comprehensive READMEs for each version

### Publications

Research findings and methodology are being prepared for academic publication. For citation information, see [Citation](#-citation) section below.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.
```
MIT License - Copyright (c) 2025 Hatice Baydemir
```

---

## 👤 Contact

**Hatice Baydemir**

- **GitHub:** [@haticebaydemir](https://github.com/haticebaydemir)
- **Institution:** Karamanoğlu Mehmetbey Üniversitesi
- **Program:** TÜBİTAK 2209-A

**Academic Advisor:** İlya Kuş

**For Research Inquiries:** Please open a GitHub issue or see contact information in the repository.

---

## 🙏 Acknowledgments

We gratefully acknowledge:

- **TÜBİTAK (The Scientific and Technological Research Council of Turkey)** for funding and support through the 2209-A Undergraduate Research Projects Support Program

- **Karamanoğlu Mehmetbey Üniversitesi** for providing institutional support and research infrastructure

- **Dataset:** [Fashion Product Images Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset) by Param Aggarwal, available on Kaggle under open license

- **Open Source Community:**
  - Hugging Face for pre-trained models (sentence-transformers, CLIP)
  - Facebook AI Research (FAIR) for FAISS vector search library
  - Microsoft for LightGBM gradient boosting framework
  - GROQ for LLM API access (v2.1+)
  - The broader Python ML/AI ecosystem

---

## 📈 Project Status

- **v2.0:** Stable baseline - Research complete ✅
- **v2.1:** GenAI enhancements - Complete ✅
- **v2.2:** RAG Pipeline - Complete ✅
- **v2.3-v2.4:** Planned 📅
- **Maintenance:** Ongoing
- **Documentation:** Comprehensive

**Last Updated:** January 3, 2026

---

<p align="center">
  <strong>TÜBİTAK 2209-A Undergraduate Research Project</strong><br>
  September 2024 - February 2025<br>
</p>

<p align="center">
  <em>Advancing fashion e-commerce through multimodal AI and GenAI technologies</em>
</p>
