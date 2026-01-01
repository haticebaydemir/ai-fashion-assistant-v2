# v2.1: Core ML + Visual Attributes & Evaluation

**Status:** ✅ COMPLETE  
**Duration:** Week 1-2 (January 1-2, 2025)  
**Focus:** Multimodal fusion optimization, visual attribute extraction, comprehensive evaluation

---

## Overview

v2.1 establishes the core machine learning foundation for the AI Fashion Assistant with optimized multimodal fusion, semantic visual attributes, and rigorous baseline comparisons.

## Key Components

### 1. Learned Fusion Model
- **Optimal α = 0.7** (70% text, 30% image weighting)
- Text-heavy weighting reflects descriptive nature of fashion queries
- Tested on 42 initial queries across multiple scenarios
- Fusion strategy: `fused = α × text_emb + (1-α) × image_emb`

### 2. Visual Attributes Extraction
- **307,720 attributes** extracted using CLIP zero-shot classification
- **6.93 avg attributes per product** (95.4% coverage)
- **10 semantic categories**: pattern, fit, length, neckline, sleeve, material, formality, season, occasion, style
- Model: CLIP ViT-Large/14 (768d embeddings)
- Confidence threshold: 0.15 (optimized for coverage-precision balance)

### 3. Explainability System
- Multimodal fusion score decomposition
- Attribute-based matching explanations
- Text vs visual contribution analysis
- Natural language explanation generation

### 4. Comprehensive Query Generation
- **104 evaluation queries** generated via GROQ Llama-3.3-70B
- **7 query categories**: simple_item, attribute_specific, occasion_based, style_based, complex_multi_attr, seasonal, budget_conscious
- **Bilingual**: 59 English + 45 Turkish
- Average query length: 3.6 words (realistic user behavior)

### 5. Baseline Comparisons & Evaluation
- **7 baseline methods** evaluated:
  1. BM25 (sparse retrieval)
  2. TF-IDF (term weighting)
  3. Text-only Dense (mpnet embeddings)
  4. Image-only Dense (CLIP embeddings)
  5. Fixed Fusion α=0.5 (equal weighting)
  6. Fixed Fusion α=0.7 (our optimal)
  7. BM25+Dense Hybrid

- **Evaluation methodology**: Reciprocal Rank Fusion (RRF) consensus ground truth
- **Metrics**: Consensus Overlap@10, Rank Correlation, Category-wise performance

### Results
- **Best method**: Fusion α=0.7 (our method)
- **Consensus Overlap@10**: 0.6779
- **Rank Correlation**: 0.8833
- Multimodal fusion outperforms all unimodal and alternative fusion strategies

---

## Project Structure
```
v2.1-core-ml-plus/
├── notebooks/
│   ├── 01_visual_attributes_extraction.ipynb          # CLIP zero-shot attribute extraction
│   ├── 02_explainability_and_query_generation.ipynb   # Explainability + LLM query gen
│   └── 03_baseline_comparisons.ipynb                  # RRF-based evaluation
├── models/
│   └── fusion_model_initial.pth                       # Learned fusion checkpoint
├── evaluation/
│   ├── queries.txt                                    # 42 initial test queries
│   └── results/
│       ├── product_attributes.csv                     # 307K attributes (long format)
│       ├── enhanced_products.csv                      # Products + attributes (wide format)
│       ├── extraction_statistics.json                 # Attribute extraction stats
│       ├── evaluation_queries_100plus.csv             # 104 evaluation queries
│       ├── queries_by_category.json                   # Queries grouped by category
│       ├── baseline_comparison_RRF.csv                # Method comparison results
│       ├── category_performance.csv                   # Category-wise analysis
│       └── evaluation_summary_RRF.txt                 # Final evaluation summary
└── README.md                                          # This file
```

---

## Key Findings

### Fusion Weighting
- α=0.7 (text-heavy) optimal for fashion domain
- Fashion queries are primarily descriptive rather than visual
- Text embeddings capture product names, materials, styles effectively
- Image embeddings complement with visual patterns and colors

### Visual Attributes
- High coverage (95.4%) with reasonable confidence (avg 0.193)
- Pattern, formality, and style categories most reliably detected
- Attributes enable fine-grained filtering and enhanced search

### Query Categories
- Complex multi-attribute queries benefit most from fusion
- Occasion-based queries rely heavily on text semantics
- Style-based queries show balanced text-image contribution

### Baseline Performance
- Dense methods significantly outperform sparse (BM25, TF-IDF)
- Multimodal fusion > single modality across all categories
- Optimal fusion (α=0.7) > equal weighting (α=0.5)

---

## Technical Details

### Models & Embeddings
- **Text encoder**: sentence-transformers/paraphrase-multilingual-mpnet-base-v2 (768d)
- **Image encoder**: CLIP ViT-Large/14 (768d)
- **Fusion dimension**: 768d (normalized)
- **Search**: FAISS IndexFlatIP (cosine similarity via inner product)

### Evaluation Setup
- **Ground truth**: RRF consensus from all 7 methods (k=60)
- **Test queries**: 104 bilingual queries across 7 categories
- **Metrics**: Overlap@10, Rank Correlation (Spearman), Category-wise performance
- **Statistical approach**: Consensus-based relative comparison

### Performance
- Search latency: <100ms (FAISS)
- Attribute extraction: ~10-15 min on A100 GPU (44,417 products)
- Evaluation runtime: ~40 min CPU (7 methods × 104 queries)

---

## Dependencies
```
torch>=2.0.0
transformers>=4.30.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
rank-bm25
scikit-learn
pandas
numpy
groq>=0.4.0
```

---

## Usage

### 1. Visual Attributes Extraction
```python
# See: notebooks/01_visual_attributes_extraction.ipynb
# Extracts 10 attribute categories using CLIP zero-shot
# Output: product_attributes.csv, enhanced_products.csv
```

### 2. Explainability
```python
# See: notebooks/02_explainability_and_query_generation.ipynb
# Generate interpretable search result explanations
# LLM-based query generation for evaluation
```

### 3. Baseline Evaluation
```python
# See: notebooks/03_baseline_comparisons.ipynb
# RRF consensus evaluation of 7 methods
# Category-wise performance analysis
```

---

## Validation

All results validated through:
- ✅ Consensus-based evaluation (RRF methodology)
- ✅ Category-wise performance analysis
- ✅ Visual inspection of top-K results
- ✅ Cross-validation across query types

---

## Next Steps (v2.3)

- RAG system integration with LangChain
- Conversational query understanding
- Multi-turn dialogue management
- Context-aware result refinement

---

## References

- CLIP: Learning Transferable Visual Models From Natural Language Supervision
- Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks
- Reciprocal Rank Fusion for combining multiple rankings
- FAISS: Efficient similarity search and clustering of dense vectors

---

**Author:** Hatice Baydemir  
**Advisor:** İlya Kuş  
**Institution:** Karamanoğlu Mehmetbey University  
**Project:** TÜBİTAK 2209-A Undergraduate Research Project
