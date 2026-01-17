# Changelog

All notable changes to the AI Fashion Assistant project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.5.0] - 2026-01-17

### Added - Full-Stack Application & User Study
- **Full-stack web application** with React 18, FastAPI, and MongoDB
- **User authentication** with JWT tokens
- **User management system** (profiles, preferences, history)
- **AI chat assistant** with Llama-3.3-70B via GROQ API
- **Favorites system** for saving preferred products
- **Search history** tracking for analytics
- **User study** with 25 participants
  - System Usability Scale (SUS) evaluation
  - Custom metrics evaluation
  - Qualitative feedback collection
- **Production deployment** on Hugging Face Spaces
- **19 application screenshots** documenting all features
- **6 database structure screenshots** showing MongoDB collections
- **Demo video** on YouTube

### Performance
- **SUS Score: 84.50 / 100 (Grade A - Excellent)** 🏆
- **92% real-world usage intent** from user study
- **88% of users rated system as "Good" or better**
- Sub-second response times maintained
- 32 active users in database
- 347 searches tracked
- 139 favorites saved

### Documentation
- Comprehensive README (39KB, 999 lines)
- User study results document
- Full-stack application README
- Quick start guide
- Feature checklist
- Setup scripts for Windows

---

## [2.4.5] - 2026-01-12

### Added - Multimodal RAG
- **Image query support** - search with product images
- **Multimodal fusion retrieval** using CLIP text + image embeddings
- **Visual-aware RAG responses** (7.6 keywords per response)
- **V2.1 attribute integration** (307K visual features)
- 6 comprehensive notebooks covering full pipeline

### Performance
- Response time: 0.64s average (28% faster than v2.2)
- 100% visual keyword generation rate
- 6.0 unique products via multimodal fusion

---

## [2.4.0] - 2026-01-05

### Added - User Features & Personalization
- **User profile system** with preferences and history
- **Content-based personalization** (3 strategies)
- **Integrated agent system** with intent awareness
- **Favorites management**
- **Search history tracking**

### Performance
- 76.7% preference matching accuracy
- Sub-12ms personalization latency (target: <50ms)
- 100% personalization coverage
- 83.3% personalization rate in agent interactions

---

## [2.3.0] - 2026-01-04

### Added - AI Agents + LangChain
- **Conversational AI agent** with ReAct reasoning
- **3 specialized tools** (SearchProducts, RecommendSimilar, GetProductDetails)
- **Conversation memory** (10-turn sliding window)
- **Multi-turn dialogue support** (5 scenarios tested)
- Complete LangChain integration (4 notebooks, 82 cells)

### Performance
- 100% success rate on test dialogues
- 100% tool usage rate
- 2.6s average response time
- Multi-turn context awareness

---

## [2.2.0] - 2026-01-03

### Added - RAG Pipeline
- **Production-ready RAG** (Retrieval-Augmented Generation)
- **FashionRAGPipeline class** with caching & batch processing
- Framework-agnostic implementation
- 3 professional notebooks (fundamentals, production, evaluation)

### Performance
- 0.714 average RAG score on 30 queries
- 0.89s response time
- Comprehensive evaluation metrics

---

## [2.1.0] - 2026-01-01

### Added - Core ML + Visual Attributes
- **Learned fusion optimization** (α=0.7)
- **Visual attribute extraction** (307K attributes, 10 categories)
- **Explainability system** with fusion decomposition
- Comprehensive query generation (104 bilingual queries)
- **7 baseline methods comparison**

### Performance
- 97.4% NDCG@10 (maintained from v2.0)
- 95.4% product coverage with visual attributes
- Attribute-aware search and reranking

---

## [2.0.0] - 2025-12-15

### Added - Stable Baseline
- **Core multimodal search system**
- Text embeddings (MPNet 768d)
- Image embeddings (CLIP 512d → 768d aligned)
- FAISS vector indexing
- 30+ research notebooks
- Production deployment pipeline
- Docker containers
- Monitoring with Prometheus + Grafana

### Performance
- **97.4% NDCG@10** baseline performance
- **100% MRR** on test queries
- **51.1% Recall@10**
- Sub-10ms retrieval latency
- 44,417 products indexed

### Dataset
- Fashion Product Images Dataset (Kaggle)
- 44,417 products
- 6 main categories
- Multilingual support (Turkish/English)

---

## [1.0.0] - 2025-09-01

### Initial Development
- Project kickoff
- Dataset acquisition
- Initial research and planning
- Literature review
- Technical feasibility study

---

## Version Naming Convention

- **v2.x**: GenAI-enhanced versions (January-February 2026)
- **v2.0**: Stable baseline (September-December 2025)
- **v1.0**: Initial development (September 2025)

Each minor version (2.1, 2.2, etc.) represents a complete feature addition documented in separate directories.

---

## Project Timeline

```
v1.0  Sep 2025       Initial development
v2.0  Dec 2025       Stable baseline (97.4% NDCG@10)
v2.1  Jan 1, 2026    Visual attributes + explainability
v2.2  Jan 3, 2026    RAG pipeline
v2.3  Jan 4, 2026    AI agents + LangChain
v2.4  Jan 5, 2026    User features + personalization
v2.4.5 Jan 12, 2026  Multimodal RAG
v2.5  Jan 17, 2026   Full-stack + user study (SUS 84.50) 🏆
```

---

## Links

- **Repository:** https://github.com/haticebaydemir/ai-fashion-assistant-v2
- **Demo:** [Hugging Face Spaces](https://huggingface.co/spaces/HaticeB/ai-fashion-assistant)
- **Dataset:** [Kaggle - Fashion Product Images](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)
- **Program:** [TÜBİTAK 2209-A](https://www.tubitak.gov.tr/tr/burslar/lisans/burs-programlari/icerik-2209-a)

---

## Contributors

- **Hatice Baydemir** - Student Researcher
- **İlya Kuş** - Academic Advisor

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Last Updated:** January 17, 2026
