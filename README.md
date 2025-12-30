# 🛍️ AI Fashion Assistant v2.0

**A production-ready multimodal fashion search system combining semantic text search, visual similarity, and learned ranking for e-commerce product discovery**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![TÜBİTAK](https://img.shields.io/badge/TÜBİTAK-2209--A-red.svg)](https://www.tubitak.gov.tr/)
[![Dataset](https://img.shields.io/badge/Dataset-Kaggle-20BEFF.svg)](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Overview

This project implements an end-to-end multimodal search system for fashion e-commerce, achieving **97.4% NDCG@10** through novel fusion of text and image embeddings. The system processes 44,417 products using state-of-the-art transformers (CLIP, mpnet) and learned ranking models.

**Key Achievements:**
- 🎯 **97.4% NDCG@10** on 22 test queries (fusion ranking)
- ⚡ **97.7% Precision@10** with 100% MRR (first-rank accuracy)
- 🔍 **51.1% Recall@10** on diverse product catalog
- 🚀 **Production-ready** with complete deployment pipeline

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────┐
│         Query Processing                         │
│  (Intent Detection, Slot Extraction)            │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│      Multimodal Embedding                       │
│  mpnet (768d) + CLIP text (512d) → 1280d       │
│  CLIP vision (768d)                             │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│         Vector Retrieval                        │
│  FAISS IndexFlatIP (cosine similarity)         │
│  44,417 products indexed                        │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│      Learned Ranking                            │
│  LightGBM fusion + Attribute-aware reranking   │
└─────────────────────────────────────────────────┘
```

---

## 📊 Dataset

**Source:** [Fashion Product Images Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)

| Statistic | Value |
|-----------|-------|
| Total Products | 44,417 |
| Master Categories | 7 |
| Sub-categories | 45 |
| Unique Colors | 46 |
| Attributes | 8 (gender, category, color, season, usage, etc.) |
| Image Format | JPG (80x60 to 2400x3200 pixels) |

**Data Structure:**
```
fashion-product-images/
├── images/           # Product images
├── styles.csv        # Product metadata
└── images.csv        # Image paths
```

---

## 🎯 Performance Metrics

### Retrieval Performance (22 Test Queries)

| Metric | Baseline | Fusion | Improvement |
|--------|----------|--------|-------------|
| **NDCG@10** | 97.30% | **97.43%** | +0.13pp |
| **NDCG@5** | 97.61% | 97.61% | - |
| **Recall@10** | 50.61% | **51.11%** | +0.50pp |
| **Recall@5** | 25.36% | 25.36% | - |
| **Precision@10** | 97.73% | 97.73% | - |
| **Precision@5** | 98.18% | 98.21% | +0.03pp |
| **MRR** | 100% | 100% | - |

### Query Type Breakdown

| Query Type | Count | NDCG@10 |
|------------|-------|---------|
| Specific | 13 | **97.84%** |
| General | 7 | **95.54%** |
| Attribute | 2 | **100%** |

**Evaluation Date:** December 19-20, 2024

---

## 🔬 Technical Implementation

### Models & Embeddings

**Text Encoding (1280-dimensional combined space):**
- Primary: `paraphrase-multilingual-mpnet-base-v2` (768d)
- Secondary: CLIP text encoder from `openai/clip-vit-base-patch32` (512d)
- Combined: Concatenated 768d + 512d = 1280d

**Image Encoding:**
- Model: CLIP vision encoder from `openai/clip-vit-base-patch32`
- Dimensions: 768d
- Preprocessing: Center crop + normalize

**Search Infrastructure:**
- Index: FAISS `IndexFlatIP` (inner product / cosine similarity)
- Vectors: 44,417 product embeddings
- Retrieval: Top-k nearest neighbors

### Ranking Pipeline

**Phase 1: Baseline Retrieval**
- Text-only: mpnet embeddings
- Image-only: CLIP vision embeddings
- NDCG@10: 97.30%

**Phase 2: Fusion Ranking**
- Method: Learned weighted fusion with LightGBM
- Features: Text similarity, image similarity, attribute matches
- NDCG@10: 97.43% (+0.13pp improvement)

**Phase 3: Personalization**
- Collaborative filtering: ALS (Alternating Least Squares)
- User embeddings: 64-dimensional latent factors
- Cold-start handling: Content-based fallback

---

## 📁 Project Structure

```
ai-fashion-assistant-v2/
├── notebooks/              # Research & development (30+ notebooks)
│   ├── phase0_setup/       # Project initialization
│   ├── phase1_foundation/  # Data prep & SSOT schema
│   ├── phase2_embeddings/  # Model selection & embedding generation
│   ├── phase3_retrieval/   # Baseline retrieval & FAISS indexing
│   ├── phase4_evaluation/  # Evaluation framework
│   ├── phase5_optimization/# Advanced ranking (LightGBM)
│   ├── phase6_advanced_features/ # Personalization (ALS)
│   ├── phase7_api_deployment/   # FastAPI + Docker
│   ├── phase8_llm_features/     # LLM experiments
│   ├── phase9_evaluation/       # Comprehensive evaluation
│   └── phase10_reproducibility/ # Final documentation
│
├── src/                    # Production Python modules
│   ├── schema.py           # SSOT data schemas
│   ├── search_engine.py    # Core search implementation
│   └── config.py           # Configuration management
│
├── models/                 # Trained models
│   ├── advanced_ranker.pkl           # LightGBM fusion model
│   ├── fusion_ranker.pkl             # Ranking model
│   ├── advanced_ranker_optimized.pkl # Optimized ranker
│   └── personalization/              # ALS collaborative filtering
│
├── data/                   # Data & schemas
│   ├── processed/          # Processed datasets
│   └── schemas/            # SSOT schema definitions
│
├── embeddings/             # Precomputed embeddings
│   └── (Stored in Google Drive)
│
├── evaluation/             # Evaluation results
│   └── baselines/          # Baseline comparisons
│
├── deployment/             # Deployment configurations
│   ├── api/                # FastAPI backend
│   ├── ui/                 # Streamlit frontend
│   ├── docker/             # Docker containerization
│   └── monitoring/         # Prometheus + Grafana
│
├── docs/                   # Documentation
│   ├── evaluation/         # Evaluation reports & charts
│   ├── results/            # Performance metrics
│   ├── reports/            # Final reports
│   ├── TUBITAK_ROADMAP.md  # Project roadmap
│   └── REPRODUCIBILITY.md  # Reproducibility guide
│
├── paper/                  # Academic paper drafts
├── tests/                  # Unit tests
├── schemas/                # Additional schemas
├── visual_search/          # Visual search experiments
├── llm/                    # LLM feature experiments
└── experiments/            # Experimental notebooks
```

---

## 🚀 Installation & Usage

### Prerequisites

- Python 3.10+
- CUDA-capable GPU (recommended for inference)
- 16GB+ RAM

### Setup

```bash
# Clone repository
git clone https://github.com/hsicakdemir/ai-fashion-assistant-v2.git
cd ai-fashion-assistant-v2

# Install dependencies
pip install -r requirements.txt
```

### Running the System

**Option 1: Jupyter Notebooks** (Recommended for exploration)
```bash
jupyter notebook
# Navigate to notebooks/phase10_reproducibility/
```

**Option 2: Google Colab** (For deployment demos)
- Upload notebooks to Google Drive
- Open in Colab and run cells sequentially
- Demo notebooks available in deployment/

---

## 🛠️ Technology Stack

### Core Libraries

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Embeddings** | sentence-transformers | Text encoding (mpnet) |
| **Vision** | transformers (CLIP) | Image encoding |
| **Search** | FAISS | Vector similarity search |
| **Ranking** | LightGBM | Learned fusion & reranking |
| **Personalization** | implicit (ALS) | Collaborative filtering |
| **Backend** | FastAPI | REST API |
| **Frontend** | Streamlit | Web UI |
| **Deployment** | Docker | Containerization |
| **Monitoring** | Prometheus + Grafana | Metrics & dashboards |

### Framework Versions

```
sentence-transformers==2.2.2
transformers==4.30.2
torch==2.0.1
faiss-gpu==1.7.2
lightgbm==4.0.0
fastapi==0.109.0
streamlit==1.28.0
```

---

## 📚 Research Phases

### Phase 0-1: Foundation
- Project setup and initialization
- Data preparation and cleaning
- SSOT (Single Source of Truth) schema definition
- Schema validation framework

### Phase 2: Embeddings
- Model selection (mpnet vs multilingual alternatives)
- Embedding generation for 44,417 products
- Hybrid embedding space creation (text 1280d + image 768d)

### Phase 3: Retrieval
- FAISS index construction (IndexFlatIP)
- Baseline retrieval implementation
- Fusion ranking experiments

### Phase 4: Evaluation
- Evaluation framework design
- Metrics implementation (NDCG, Recall, MRR)
- Baseline performance measurement

### Phase 5: Optimization
- Advanced ranking with LightGBM
- Hyperparameter tuning
- Ablation studies

### Phase 6: Advanced Features
- Personalization with collaborative filtering (ALS)
- User profile embeddings
- Similar items recommendation

### Phase 7: API & Deployment
- FastAPI production API
- Docker containerization
- Monitoring setup (Prometheus + Grafana)

### Phase 8: LLM Features (Experimental)
- LLM integration for query understanding
- Multi-turn dialogue experiments
- Query rewriting
- Explainability

### Phase 9: Comprehensive Evaluation
- Full evaluation on 22 diverse test queries
- Query type analysis
- Baseline comparisons

### Phase 10: Reproducibility
- Schema standardization
- Documentation completion
- Reproducibility validation

---

## 🎓 Academic Context

**Program:** TÜBİTAK 2209-A Undergraduate Research Projects Support Program

**Institution:** Karamanoğlu Mehmetbey Üniversitesi

**Student Researcher:** Hatice Baydemir

**Advisor:** İlya Kuş

**Duration:** September 2024 - December 2024

### Key Contributions

1. **High-Performance Multimodal Search**
   - Achieved 97.4% NDCG@10 on fashion product search
   - Novel fusion approach combining semantic and visual signals

2. **Production-Ready Implementation**
   - Complete end-to-end pipeline from data to deployment
   - Reproducible research with SSOT framework

3. **Comprehensive Evaluation**
   - Rigorous evaluation on 22 diverse test queries
   - Query type analysis and baseline comparisons

4. **Open Source Contribution**
   - Fully documented codebase
   - Reproducibility guides and deployment configs

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Contact

**Hatice Baydemir**
- GitHub: [@haticebaydemir](https://github.com/haticebaydemir)
- Institution: Karamanoğlu Mehmetbey Üniversitesi
- Program: TÜBİTAK 2209-A

**Advisor:** İlya Kuş

---

## 🙏 Acknowledgments

- **TÜBİTAK** for funding through the 2209-A Undergraduate Research Program
- **Dataset:** [Fashion Product Images Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset) by Param Aggarwal (Kaggle)
- **Hugging Face** for providing pre-trained models (sentence-transformers, CLIP)
- **Facebook AI Research** for FAISS vector search library
- **Microsoft** for LightGBM gradient boosting framework



---

<p align="center">
  <strong>TÜBİTAK 2209-A Undergraduate Research Project</strong><br>2025<br>
</p>
