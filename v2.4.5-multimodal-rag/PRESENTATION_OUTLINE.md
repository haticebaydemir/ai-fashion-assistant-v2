# v2.4.5 Presentation Outline

**Duration:** 20 minutes  
**Audience:** Academic committee, TÜBİTAK reviewers

---

## Slide 1: Title Slide
- Project: AI Fashion Assistant v2.4.5
- Subtitle: Multimodal RAG for Fashion Search
- Student: Hatice Baydemir
- Advisor: İlya Kuş
- Institution: Karamanoğlu Mehmetbey University
- Date: January 2026

---

## Slide 2: Problem Statement (2 min)
- Traditional fashion search: Text-only, limited
- User needs: "Find items like this image"
- Gap: No multimodal fashion search for Turkish market
- Visual attributes matter but ignored in text search

---

## Slide 3: Project Evolution (2 min)
**Timeline graphic:**
- v2.0: Text baseline (NDCG@10: 0.974)
- v2.1: Visual features (307K attributes)
- v2.2: RAG system (0.89s response)
- v2.4: Personalization (76.7% match)
- **v2.4.5: Multimodal RAG** ← We are here

---

## Slide 4: System Architecture (3 min)
**Architecture diagram:**
- Query Processing (CLIP)
- Multimodal Retrieval (FAISS)
- Attribute Filtering (V2.1)
- Visual-Aware RAG (GROQ)

**Key Innovation:** Learned fusion α=0.7

---

## Slide 5: Technical Implementation (3 min)
**Components:**
- CLIP ViT-L/14 (768d embeddings)
- FAISS HNSW indexing
- 44,417 products indexed
- GROQ Llama-3.3-70B

**Challenges Solved:**
- CLIP text encoding for 44K products (~25 min)
- Embedding space consistency
- Attribute integration (307K → 44K mapping)

---

## Slide 6: Key Results (4 min)
**Performance Metrics:**
| Metric | Value |
|--------|-------|
| Multimodal Unique | 6.0 products |
| Response Time | 0.64s (28% faster) |
| Visual Keywords | 7.6 per response |
| Overlap Rate | 4.0% |

**Show: 4-panel visualization**

---

## Slide 7: Example Query Demo (3 min)
**Live demo or screenshots:**
1. Text query: "white shirts"
2. Image query: Upload product image
3. Multimodal: Fusion results
4. RAG response with visual reasoning

**Highlight:** Visual keywords in response

---

## Slide 8: Comparison with Baselines (2 min)
**Table:**
| Version | Retrieval | Visual Aware | Response Time |
|---------|-----------|--------------|---------------|
| v2.0 | Text-only | No | - |
| v2.2 | Text-only | No | 0.89s |
| v2.4.5 | Multimodal | Yes (7.6) | 0.64s |

**Improvement:** +100% visual awareness, +28% speed

---

## Slide 9: Academic Contribution (1 min)
**Novel aspects:**
1. First multimodal fashion search for Turkish dataset
2. Learned fusion strategy (α=0.7)
3. Visual-aware RAG integration
4. Production-ready system (<1s response)

---

## Slide 10: Future Work & Conclusion (1 min)
**Next steps:**
- User study (20-25 participants, Week 2-3)
- Statistical validation
- Conference paper submission (RecSys/SIGIR 2026)

**Conclusion:**
✅ Multimodal RAG successfully implemented  
✅ Visual awareness achieved  
✅ Ready for user validation  

---

## Q&A (3 min)
**Anticipated questions:**
1. Why is overlap low (0.4)?
   → Different search strategies capture complementary info
2. How does fusion weight α=0.7 compare to 0.5?
   → Empirically derived from v2.1, text more reliable
3. Scalability to larger datasets?
   → FAISS HNSW supports millions, CLIP encoding parallelizable

---

**Backup Slides:**
- Detailed architecture diagram
- Full statistics table
- Code snippets
- Related work comparison
