# v2.2: RAG (Retrieval-Augmented Generation)

**Status:** ✅ COMPLETE  
**Date:** January 2, 2026  
**Focus:** Production-ready RAG pipeline for fashion search

---

## Overview

Implemented a complete RAG (Retrieval-Augmented Generation) system that combines vector search with LLM-based generation for natural language fashion product recommendations.

**Key Achievement:** 0.714 average retrieval score across 30 diverse queries with sub-second response times.

---

## System Architecture
```
User Query
    ↓
[1. RETRIEVE] → FAISS vector search (44,417 products)
    ↓
[2. AUGMENT] → Context injection into prompt
    ↓
[3. GENERATE] → GROQ LLM (Llama-3.3-70B)
    ↓
Natural Language Recommendation
```

---

## Implementation

### Three Professional Notebooks

**01_rag_fundamentals.ipynb** (21 cells)
- RAG concepts and implementation
- From-scratch pipeline
- Test queries and validation

**02_production_pipeline.ipynb** (18 cells)
- Production `FashionRAGPipeline` class
- Response caching
- Batch processing
- Statistics tracking

**03_evaluation.ipynb** (23 cells)
- 30-query comprehensive evaluation
- Category-wise analysis
- Performance metrics
- Visualizations

### Production Code

**rag_pipeline.py** (8.6KB)
- Complete production-ready class
- Clean API interface
- Configurable parameters
- Cache management

---

## Performance Metrics

### Overall Results (30 queries)

| Metric | Value |
|--------|-------|
| Average Score | 0.714 |
| Score Range | 0.554 - 0.841 |
| Std Deviation | 0.079 |
| Avg Response Time | 0.89s |

### By Category

| Category | Avg Score | Queries |
|----------|-----------|---------|
| **Simple Items** | 0.758 ⭐ | 10 |
| Specific Needs | 0.731 | 10 |
| Occasion-based | 0.653 | 10 |

**Best Query:** "pink dress" (0.841)  
**Most Challenging:** "outfit for job interview" (0.554)

---

## Project Structure
```
v2.2-rag-langchain/
├── notebooks/
│   ├── 01_rag_fundamentals.ipynb      # RAG basics
│   ├── 02_production_pipeline.ipynb   # Production class
│   └── 03_evaluation.ipynb            # Comprehensive eval
│
├── src/
│   └── rag_pipeline.py                # Production code
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
└── README.md                          # This file
```

---

## Technologies

**Core Stack:**
- **GROQ** - LLM API (Llama-3.3-70B)
- **Sentence Transformers** - Text embeddings (768d)
- **FAISS** - Vector similarity search
- **NumPy/Pandas** - Data processing

**No LangChain:** Custom implementation for:
- ✅ Full control over pipeline
- ✅ Minimal dependencies (4 packages)
- ✅ Better debugging
- ✅ Production flexibility

---

## Usage

### Basic Query
```python
from src.rag_pipeline import FashionRAGPipeline

# Initialize
pipeline = FashionRAGPipeline(
    metadata_path="data/processed/meta_ssot.csv",
    embeddings_path="v2.0-baseline/embeddings/text/mpnet_768d.npy",
    groq_api_key="your_key"
)

# Query
result = pipeline.query("blue summer dress")
print(result['answer'])
# Output: Natural language recommendation with specific products
```

### Batch Processing
```python
queries = ["red dress", "black shoes", "winter jacket"]
results = pipeline.batch_query(queries)
```

### With Caching
```python
# Automatic caching enabled by default
result1 = pipeline.query("blue shirt")  # API call
result2 = pipeline.query("blue shirt")  # Cache hit (instant)

# Statistics
stats = pipeline.get_stats()
print(f"Cache hit rate: {stats['cache_hit_rate']:.1%}")
```

---

## Key Insights

### What Works Best

1. **Simple item queries** (0.758 avg)
   - Direct color + item combinations
   - Clear product specifications
   - Example: "pink dress", "white sneakers"

2. **Specific need queries** (0.731 avg)
   - Functional requirements
   - Attribute-based searches
   - Example: "running shoes with support"

### Challenging Areas

1. **Occasion-based queries** (0.653 avg)
   - Abstract requirements
   - Multiple attribute matching needed
   - Example: "outfit for job interview"

**Insight:** System performs best with concrete product descriptions, less well with abstract contexts.

---

## Technical Details

### Retrieval

- **Method:** Cosine similarity via FAISS IndexFlatIP
- **Embeddings:** Pre-normalized 768d vectors
- **Index size:** 44,417 products
- **Latency:** <100ms

### Generation

- **Model:** Llama-3.3-70B-Versatile (GROQ)
- **Temperature:** 0.1 (low for consistency)
- **Max tokens:** 500
- **Average time:** ~0.8s per query

### Pipeline

- **Cache:** In-memory dict (persistent via JSON)
- **Batch support:** Sequential processing
- **Error handling:** Graceful degradation
- **Statistics:** Query count, cache hits, response times

---

## Comparison: Manual vs LangChain

**Our Approach (Framework-Agnostic):**

✅ **Pros:**
- Lightweight (4 dependencies)
- Full control over pipeline
- Easy debugging
- No dependency conflicts
- Production-ready

❌ **Cons:**
- Manual implementation effort
- No ecosystem integrations

**LangChain Alternative:**

✅ **Pros:**
- Industry standard
- Rich ecosystem
- Pre-built components

❌ **Cons:**
- Heavy framework (50+ dependencies)
- Dependency hell (experienced during dev)
- Less flexibility
- Harder debugging

**Decision:** Manual implementation chosen for stability, control, and production requirements. LangChain integration can be added as optional module.

---

## Evaluation Methodology

**Test Set Design:**
- 30 queries across 3 categories
- Balanced distribution (10 per category)
- Real-world query patterns

**Metrics:**
- Retrieval score (cosine similarity)
- Response time (end-to-end)
- Category-wise breakdown
- Statistical analysis

**Ground Truth:**
- Vector similarity as proxy
- Manual validation of top results
- Category appropriateness check

---

## Dependencies
```
groq>=0.4.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
numpy>=1.24.0
pandas>=2.0.0
```

**Total:** 5 core packages (minimal footprint)

---

## Reproducibility

All notebooks include:
- Clear cell-by-cell execution flow
- Inline documentation
- Expected outputs
- API key placeholders
- Error handling

**To reproduce:**
1. Set GROQ API key
2. Run notebooks sequentially (01 → 02 → 03)
3. Results automatically saved to `evaluation/results/`

---

## Performance Optimization

**Implemented:**
- ✅ Pre-normalized embeddings
- ✅ FAISS IndexFlatIP (fastest)
- ✅ Response caching
- ✅ Batch processing

**Potential improvements:**
- [ ] Async LLM calls
- [ ] GPU acceleration for embeddings
- [ ] Redis cache for distributed systems
- [ ] Query preprocessing/normalization

---

## Author
**Hatice Baydemir**  
Karamanoğlu Mehmetbey University

**TÜBİTAK 2209-A Project**  
Advisor: İlya Kuş



---

**Version:** v2.2-complete  
**Last Updated:** January 3, 2025  
**Status:** Production-ready ✅
