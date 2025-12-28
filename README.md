# 🛍️ AI Fashion Assistant v2.0

**An end-to-end multimodal conversational AI system for e-commerce product search and recommendation**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)]()

---

## 🎯 Project Overview

This project implements a **production-grade multimodal search and recommendation system** that combines:

- **🔍 Multimodal Retrieval:** Text + Image hybrid search using CLIP and sentence transformers
- **🧠 LLM-powered Understanding:** Intent detection, slot extraction, and query rewriting
- **📊 Learned Ranking:** ML-based fusion and attribute-aware reranking
- **💬 Conversational Interface:** Multi-turn dialogue with memory and tool calling
- **👤 Personalization:** User profiles, favorites, and personalized recommendations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│           LAYER 3: PERSONALIZATION                      │
│  (User Profile, Favorites, Click Tracking, Reranking)   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│      LAYER 2: REASONING & DIALOGUE (LLM)                │
│  (Intent, Slots, Multi-turn Memory, Tool Calling)       │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│         LAYER 1: RETRIEVAL (Multimodal)                 │
│  (Text, Image, Hybrid, Learned Fusion, Attr-Aware)      │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Key Features

### **1. Multimodal Search**
- **Text Search:** Multilingual semantic search (Turkish + English)
- **Image Search:** Visual similarity using CLIP
- **Hybrid Search:** Learned fusion of text and image signals

### **2. Query Understanding**
- **Intent Detection:** search, filter, compare, recommend, combine
- **Slot Extraction:** color, gender, category, price, brand, etc.
- **Query Rewriting:** LLM-powered multi-variant expansion

### **3. Advanced Ranking**
- **Phase G:** Learned fusion with LightGBM
- **Phase H:** Attribute-aware reranking with confidence estimation
- **Explainability:** Counterfactual explanations for rankings

### **4. Personalization**
- User profile embeddings
- Favorite-based recommendations
- Click history and behavioral signals
- Cold-start onboarding

### **5. Conversational AI**
- Multi-turn dialogue with state management
- Tool calling (search, rerank, explain)
- Natural language responses
- Reference resolution ("that red one", "cheaper options")

---

## 📁 Project Structure

```
ai_fashion_assistant_v2/
├── notebooks/          # Jupyter notebooks (research & development)
│   ├── phase0_setup/
│   ├── phase1_foundation/
│   ├── phase2_embeddings/
│   ├── phase3_retrieval/
│   ├── phase4_understanding/
│   ├── phase5_ranking/
│   ├── phase6_personalization/
│   ├── phase7_evaluation/
│   ├── phase8_chatbot/
│   ├── phase9_deployment/
│   └── phase10_final/
│
├── src/                # Production Python modules
│   ├── schema.py       # SSOT schema definitions
│   ├── embedding_engine.py
│   ├── search_engine.py
│   ├── query_processor.py
│   ├── llm_controller.py
│   └── ...
│
├── api/                # FastAPI backend
├── ui/                 # Streamlit frontend
├── configs/            # YAML configurations
├── tests/              # Unit tests
└── docs/               # Documentation
```

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.10+
- CUDA-capable GPU (recommended)
- 16GB+ RAM

### **Installation**

```bash
# Clone repository
git clone https://github.com/yourusername/ai-fashion-assistant-v2.git
cd ai-fashion-assistant-v2

# Setup environment
make setup

# Or manually:
pip install -r requirements.txt
```

### **Run Demo**

```bash
# Start API server
make api

# Start UI (in another terminal)
make ui

# Or run end-to-end demo notebook
jupyter notebook notebooks/phase10_final/01_end_to_end_demo.ipynb
```

---

## 📊 Dataset

**Fashion Product Images Dataset**
- **44,418 products** with images and metadata
- **8 categorical attributes:** category, gender, color, season, usage, etc.
- **Languages:** Turkish and English product descriptions

---

## 🎯 Performance Metrics

### **Retrieval Performance**

| Method | Hit@5 | Hit@10 | MRR | NDCG@10 |
|--------|-------|--------|-----|---------|
| Text-only | 0.72 | 0.82 | 0.58 | 0.68 |
| Image-only | 0.78 | 0.87 | 0.63 | 0.73 |
| Hybrid (α=0.5) | 0.84 | 0.91 | 0.69 | 0.79 |
| + Query Rewrite | 0.87 | 0.93 | 0.72 | 0.82 |
| + Learned Fusion | 0.89 | 0.95 | 0.75 | 0.85 |

### **System Performance**
- **API Latency (p95):** <200ms
- **Throughput:** >10 QPS (single GPU)
- **Embedding Generation:** ~5ms per text, ~30ms per image

---

## 🔧 Technology Stack

### **Models**
- **Text:** `paraphrase-multilingual-mpnet-base-v2` (768d)
- **Text (Secondary):** CLIP text encoder (512d)
- **Image:** CLIP ViT-Large/14 (768d)
- **LLM:** GPT-3.5-turbo / Mistral-7B

### **Frameworks**
- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **ML:** PyTorch, Transformers, sentence-transformers
- **Ranking:** LightGBM, XGBoost
- **Search:** FAISS (HNSW)

---

## 📚 Documentation

- [**Architecture Guide**](docs/architecture.md) - System design and components
- [**Methodology**](docs/methodology.md) - Technical approach and algorithms
- [**API Reference**](docs/api_reference.md) - API endpoints and usage
- [**SSOT Specification**](docs/ssot_specification.md) - Schema definitions

---

## 🎓 Academic Contributions

This project is submitted to **TÜBİTAK 2209-A Research Program**.

**Key Innovations:**
1. **Multimodal Fusion with Confidence:** Adaptive hard/soft constraints
2. **Explainable Ranking:** Counterfactual explanations for reranking
3. **LLM Tool Calling:** Function-calling-based search orchestration
4. **Personalization:** User embedding-based reranking

---

## 📈 Roadmap

- [x] Phase 0-1: Foundation + SSOT
- [x] Phase 2: Multimodal embeddings
- [x] Phase 3: Retrieval + Phase G fusion
- [x] Phase 4: LLM query understanding
- [x] Phase 5: Phase H attribute-aware ranking
- [x] Phase 6: Personalization
- [x] Phase 7: Comprehensive evaluation
- [x] Phase 8: Chatbot + deployment


---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- TÜBİTAK for funding and support
- Fashion Product Images Dataset contributors
- OpenAI, Anthropic, and Hugging Face for model access

---

## 📊 Citation

If you use this project in your research, please cite:

```bibtex
@misc{ai_fashion_assistant_v2,
  author = {Your Name},
  title = {AI Fashion Assistant v2.0: Multimodal Conversational Search},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/yourusername/ai-fashion-assistant-v2}
}
```

---

<p align="center">Made with ❤️ for AI-powered e-commerce</p>
