# 🛍️ AI Fashion Assistant v2.0

**A production-ready multimodal fashion search system achieving 97.4% NDCG@10 through novel fusion of text and image embeddings**

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
- 📊 **22 diverse test queries** - Comprehensive evaluation coverage
- 🚀 **Production-ready** - Complete deployment pipeline included

---

## 🏗️ System Architecture

The system implements a four-stage pipeline optimized for fashion e-commerce:

```
┌─────────────────────────────────────────────────┐
│         1. Query Processing                     │
│    Intent Detection • Slot Extraction           │
│    Multi-language Support (TR/EN)               │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│      2. Multimodal Embedding                    │
│    Text: mpnet (768d) + CLIP text (512d)       │
│    Image: CLIP vision (768d)                    │
│    Combined Space: 1280-dimensional             │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│         3. Vector Retrieval (FAISS)             │
│    IndexFlatIP • Cosine Similarity              │
│    44,417 products • <10ms latency              │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│      4. Learned Ranking (LightGBM)              │
│    Feature Fusion • Attribute Awareness         │
│    Personalization • Reranking                  │
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
| Image Resolution | 80×60 to 2400×3200 pixels |
| File Format | JPG images + CSV metadata |
| Total Size | ~4.5 GB |

---

## 🎯 Performance Metrics

### Final Evaluation Results (December 19-20, 2025)

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

### Performance by Query Type

| Query Type | Examples | Count | NDCG@10 |
|------------|----------|-------|---------|
| **Specific** | "Nike red running shoes", "Adidas blue jacket" | 13 | **97.84%** |
| **General** | "summer dresses", "casual shoes" | 7 | **95.54%** |
| **Attribute** | "blue jeans for men", "black formal shoes" | 2 | **100%** |

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
- **Model:** OpenAI CLIP ViT-B/32 vision encoder (768d)
- **Preprocessing:** Center crop, normalize to ImageNet statistics

### Search Infrastructure

**Vector Index:**
- **Type:** FAISS IndexFlatIP (inner product / cosine similarity)
- **Size:** 44,417 product embeddings
- **Latency:** <10ms retrieval (p95)
- **Storage:** Optimized for memory-mapped files

**Ranking Pipeline:**
1. **Baseline Retrieval:** Direct cosine similarity (NDCG@10: 97.30%)
2. **Learned Fusion:** LightGBM ranker with features:
   - Text similarity score
   - Image similarity score
   - Attribute match indicators
   - Historical popularity
   - **Result:** NDCG@10: 97.43%
3. **Personalization (Optional):** ALS collaborative filtering with 64d user embeddings

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

## 📚 Research Phases

The project was developed in 10 phases over 4 months (September-December 2025):

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

**📖 Detailed phase documentation:** See [`v2.0-baseline/research/notebooks/`](./v2.0-baseline/research/notebooks/)

---

## 🎓 Academic Context

### Research Program

**Program:** TÜBİTAK 2209-A Undergraduate Research Projects Support Program

**Duration:** September 2025 - December 2025

**Student Researcher:** Hatice Baydemir

**Advisor:** İlya Kuş

### Key Contributions

1. **Novel Multimodal Fusion Strategy**
   - Learned fusion of semantic (mpnet) and visual (CLIP) embeddings
   - Achieves 97.4% NDCG@10 on fashion product search
   - Outperforms text-only and image-only baselines

2. **Production-Ready Implementation**
   - Complete end-to-end pipeline from raw data to deployment
   - SSOT (Single Source of Truth) framework for reproducibility
   - 30+ documented notebooks covering all development phases

3. **Comprehensive Evaluation Framework**
   - Rigorous evaluation on 22 diverse test queries
   - Query type analysis (specific, general, attribute-based)
   - Multiple baseline comparisons and ablation studies

4. **Open Source Release**
   - Fully documented codebase with reproducibility guides
   - Clean separation of research and production code
   - Deployment configs for Docker and cloud platforms

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
  - The broader Python ML/AI ecosystem

---


---

## 📈 Project Status

- **v2.0 (Current):** Stable baseline - Research complete ✅
- **Development:** Active
- **Maintenance:** Ongoing
- **Documentation:** Complete

**Last Updated:** December 30, 2025

---

<p align="center">
  <strong>TÜBİTAK 2209-A Undergraduate Research Project</strong><br>
  2025<br>
</p>

<p align="center">
  <em>Advancing fashion e-commerce through multimodal AI</em>
</p>

