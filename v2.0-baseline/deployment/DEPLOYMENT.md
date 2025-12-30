# 🚀 Deployment Guide - E-Commerce Chatbot Demo

## 📋 Overview

This guide explains how to deploy and run the AI Fashion Assistant v2.0 demo using the provided Colab notebook.

**Demo Notebook:** `E_Ticaret_Chatbot_DEMO.ipynb`

**Components:**
- FastAPI backend with search endpoints
- Streamlit frontend interface
- ngrok tunnel for public access
- FAISS vector search with 44,417 products

---

## ⚙️ Prerequisites

### Required:
- Google Account (for Colab)
- ngrok Account (free tier) - [Sign up here](https://ngrok.com/)
- Google Drive with sufficient space (~2GB for models/embeddings)

### Optional:
- CUDA-capable GPU (for faster inference)
- Premium Colab (for better GPU access)

---

## 📦 Setup Steps

### 1. Get ngrok Token

1. Go to [ngrok.com](https://ngrok.com/)
2. Sign up / Log in
3. Go to **"Your Authtoken"** section
4. Copy your authtoken

### 2. Prepare Google Drive

**Required Files in Google Drive:**

```
/MyDrive/ai-fashion-assistant-v2/
├── models/
│   ├── mpnet_model/              # sentence-transformers model
│   ├── clip_model/               # CLIP model
│   └── advanced_ranker.pkl       # LightGBM ranker
│
├── embeddings/
│   ├── text_embeddings.npy       # Text embeddings (44,417 x 1280)
│   └── image_embeddings.npy      # Image embeddings (44,417 x 768)
│
├── data/
│   └── styles_processed.csv      # Product metadata
│
└── faiss_index/
    └── product_index.faiss       # FAISS index
```

**Note:** These files should already exist from your v2.0 baseline research. If not, run the preprocessing notebooks first.

### 3. Upload Notebook to Colab

1. Go to [Google Colab](https://colab.research.google.com/)
2. **File** → **Upload notebook**
3. Upload `E_Ticaret_Chatbot_DEMO.ipynb`
4. Connect to runtime: **Runtime** → **Change runtime type** → **GPU** (T4 recommended)

---

## 🎯 Running the Demo

### Step-by-Step Execution:

#### Cell 1: Drive Mount
```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')
```
**Action:** Click authorization link, sign in, copy code, paste

---

#### Cell 2: System Setup
```python
# Install system dependencies
!apt-get update -qq
!apt-get install -y -qq python3-opencv
```
**Wait for:** Installation to complete (~30 seconds)

---

#### Cell 3: Install Packages
```python
# Install Python packages
!pip install -q fastapi uvicorn pyngrok streamlit ...
```
**Wait for:** Package installation (~2 minutes)

---

#### Cell 4-8: Backend Setup
These cells load models, embeddings, and create the FastAPI backend.

**No action needed** - Just run sequentially

**Watch for:**
- ✅ Models loaded successfully
- ✅ FAISS index loaded (44,417 vectors)
- ✅ Backend initialized

---

#### Cell 9: Configure ngrok ⚠️ **ACTION REQUIRED**

```python
from pyngrok import ngrok

NGROK_TOKEN = "YOUR_NGROK_TOKEN_HERE"  # ← REPLACE THIS!

ngrok.set_auth_token(NGROK_TOKEN)
print("✅ ngrok yapılandırıldı!")
```

**Action:** Replace `YOUR_NGROK_TOKEN_HERE` with your actual ngrok token

---

#### Cell 10-12: Streamlit Frontend Setup

These cells create the Streamlit UI.

**No action needed** - Just run sequentially

---

#### Cell 13: Start Services 🚀

```python
# Start FastAPI backend + Streamlit frontend + ngrok tunnel
```

**This cell will:**
1. Start FastAPI on port 8000
2. Start Streamlit on port 8501
3. Create ngrok tunnel
4. Print public URL

**Output:**
```
🚀 Backend çalışıyor: http://localhost:8000
🎨 Frontend çalışıyor: http://localhost:8501

🌐 Dışarıdan erişim için ngrok URL'si:
https://xxxx-xxxx-xxxx.ngrok-free.app

✅ Sistem hazır! URL'ye tıklayarak erişebilirsiniz.
```

**Action:** Click the ngrok URL to access the demo!

---

#### Cell 14: Cleanup (Optional)

```python
# Stop services and clean up
```

Run this when you're done to free resources.

---

## 🎨 Using the Interface

### Main Interface Features:

1. **Search Box**
   - Enter product queries in Turkish or English
   - Examples: "kırmızı elbise", "nike running shoes"

2. **Filters**
   - Gender: Erkek, Kadın, Unisex
   - Category: Giyim, Ayakkabı, Aksesuar, etc.
   - Color: Kırmızı, Mavi, Siyah, etc.
   - Season: Yaz, Kış, Sonbahar, İlkbahar

3. **Search Type**
   - Text Search: Semantic search using mpnet + CLIP
   - Image Search: Upload image for visual similarity
   - Hybrid Search: Combination of text + image

4. **Results**
   - Product images with metadata
   - Similarity scores
   - Product details (name, color, category, etc.)

---

## 🔧 Troubleshooting

### Issue: "ngrok token invalid"
**Solution:** 
1. Check token is correct (no extra spaces)
2. Get new token from ngrok dashboard
3. Update Cell 9 and re-run

---

### Issue: "Models not found"
**Solution:**
1. Check Google Drive paths are correct
2. Ensure all model files are uploaded
3. Re-run Phase 2 notebooks to generate embeddings

---

### Issue: "CUDA out of memory"
**Solution:**
1. Restart runtime: **Runtime** → **Restart runtime**
2. Use smaller batch size
3. Use CPU-only mode (slower but works)

---

### Issue: "ngrok tunnel failed"
**Solution:**
1. Run cleanup cell (Cell 14)
2. Wait 30 seconds
3. Re-run ngrok setup (Cell 9)
4. Re-run services (Cell 13)

---

### Issue: "Port already in use"
**Solution:**
```python
# Kill existing processes
!pkill -9 uvicorn
!pkill -9 streamlit
!pkill -9 ngrok
```
Then re-run service cells

---

## 📊 Performance Tips

### For Faster Response:

1. **Use GPU Runtime**
   - T4 GPU (free tier)
   - V100/A100 (premium tier)

2. **Optimize Batch Size**
   - Smaller batches = less memory
   - Default: 32 products per search

3. **Cache Embeddings**
   - Embeddings are precomputed
   - Only query embedding is generated on-the-fly

4. **Use FAISS Efficiently**
   - Default: top-10 retrieval
   - Increase for more results (slower)

---

## 🔒 Security Notes

### Important:

1. **Never commit ngrok tokens to GitHub**
   - Tokens are personal and should be kept secret
   - Replace with placeholder before sharing

2. **ngrok URLs are temporary**
   - URLs expire when session ends
   - New URL generated each time

3. **Rate Limits**
   - Free ngrok: Limited requests/minute
   - Free Colab: Session timeout after 12 hours

4. **Data Privacy**
   - Demo runs in your Colab instance
   - No data leaves your environment
   - ngrok only tunnels requests

---

## 📈 Expected Performance

### System Specs (Colab T4 GPU):

| Metric | Value |
|--------|-------|
| **Startup Time** | ~3-5 minutes |
| **Search Latency** | <200ms (p95) |
| **Embedding Generation** | ~50ms per query |
| **FAISS Retrieval** | ~10ms for top-10 |
| **Total Response Time** | ~100-150ms |

### Search Quality:

| Metric | Value |
|--------|-------|
| **NDCG@10** | 97.43% |
| **Recall@10** | 51.11% |
| **Precision@10** | 97.73% |
| **MRR** | 100% |

---

## 📝 Demo Checklist

Before starting demo:

- [ ] Google Drive files uploaded
- [ ] ngrok token obtained
- [ ] Colab GPU runtime selected
- [ ] All cells executed in order
- [ ] ngrok URL generated
- [ ] Interface accessible

During demo:

- [ ] Search works (text queries)
- [ ] Filters work (gender, category, etc.)
- [ ] Results display correctly
- [ ] Performance is acceptable (<300ms)

---

## 🎓 Academic Use

This demo is part of:
- **Program:** TÜBİTAK 2209-A
- **Institution:** Karamanoğlu Mehmetbey Üniversitesi
- **Student:** Hatice Baydemir
- **Advisor:** İlya Kuş

For academic presentations:
1. Run demo beforehand to test
2. Share ngrok URL with audience
3. Prepare example queries
4. Have backup screenshots ready

---

## 📞 Support

**Issues or Questions?**

1. Check troubleshooting section above
2. Review v2.0-baseline notebooks for details
3. Check GitHub issues for common problems

**For Research Inquiries:**
- See main README.md for contact information

---

## 🔄 Updating the Demo

To use latest models/embeddings:

1. Re-run Phase 2 notebooks (embeddings)
2. Re-run Phase 5 notebooks (ranker)
3. Upload new files to Drive
4. Update paths in Cell 4-5 if needed
5. Restart and re-run demo

---

**Version:** 2.0 Demo

**Last Updated:** December 30, 2024

**Status:** ✅ Stable and tested
