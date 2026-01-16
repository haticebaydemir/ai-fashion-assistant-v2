# 🎨 AI Fashion Assistant - Windows Edition

![AI Fashion Assistant](../screenshots/Anasayfa.jpg)

**Modern AI-powered fashion search and recommendation system with personalization**
## Watch Full Demo Video
[![Watch Full Demo Video](../screenshots/Anasayfa.jpg)](https://www.youtube.com/watch?v=RGvt3QTJjcg)


---

## 🚀 HIZLI BAŞLANGIÇ (5 ADIM)

### 1️⃣ Data Dosyalarını Kopyala
```cmd
cd backend
copy_data.bat
(Eski proje yolunu gir)
```

### 2️⃣ Backend Kur
```cmd
cd backend
setup_backend.bat
```

### 3️⃣ Backend Başlat
```cmd
cd backend
run_backend.bat
```

### 4️⃣ Frontend Kur
```cmd
cd frontend
setup_frontend.bat
```

### 5️⃣ Frontend Başlat
```cmd
cd frontend
run_frontend.bat
```

**Tarayıcıda aç:** http://localhost:5173 🎉

---

## 📸 Application Screenshots

### 🏠 Home & Authentication

<table>
<tr>
<td width="50%">

#### Welcome Page
![Home Page](../screenshots/Anasayfa.jpg)
*Landing page with feature overview*

</td>
<td width="50%">

#### Personalized Home
![Personalized Home](../screenshots/Anasayfa2.jpg)
*After login with personalization active*

</td>
</tr>
</table>

<table>
<tr>
<td width="50%">

#### Login Page
![Login](../screenshots/LoginPage.jpg)
*Secure authentication with JWT*

</td>
<td width="50%">

#### Create Account
![Register](../screenshots/CreateAccount.jpg)
*User registration with validation*

</td>
</tr>
</table>

---

### 🔍 Search Features

#### Text Search
![Text Search](../screenshots/TextSearchWithResults.jpg)
*Semantic search powered by MPNet embeddings - Search "red cap" and get personalized results*

#### Image Search
<table>
<tr>
<td width="50%">

![Image Search Interface](../screenshots/İmageSearch.jpg)
*Upload an image to find similar products*

</td>
<td width="50%">

![Image Search Results](../screenshots/İmageSearchResults.jpg)
*CLIP-powered visual similarity search*

</td>
</tr>
</table>

#### Multimodal Search
![Multimodal Search](../screenshots/MultimodalSearch.jpg)
*Combine text and image for better results - "black shoes" + reference image*

---

### 💬 AI Chat Assistant

<table>
<tr>
<td width="50%">

#### Chat in Turkish
![Chat Turkish](../screenshots/ChatbotTC.jpg)
*Natural conversation in Turkish with product recommendations*

</td>
<td width="50%">

#### Chat in English
![Chat English](../screenshots/Ekran_AlıntısıChatbot.PNG)
*Llama-3.3-70B powered responses with personalization*

</td>
</tr>
</table>

---

### 👤 User Features

<table>
<tr>
<td width="50%">

#### My Favorites
![Favorites](../screenshots/Favorites.jpg)
*Save and manage your favorite products*

</td>
<td width="50%">

#### Profile & Preferences
![Profile](../screenshots/Profile.jpg)
*Set style preferences, sizes, and favorite colors for personalized results*

</td>
</tr>
</table>

---

## 📋 Gereksinimler

### Python 3.10+
- İndir: https://www.python.org/downloads/
- ⚠️ Kurulumda "Add to PATH" seçeneğini işaretle

### Node.js 18+
- İndir: https://nodejs.org/
- LTS versiyonunu seç

### MongoDB
**Seçenek A: Yerel MongoDB**
- İndir: https://www.mongodb.com/try/download/community
- Windows Service olarak kur
- services.msc'de başlat

**Seçenek B: MongoDB Atlas (Bulut - Önerilen)**
- https://www.mongodb.com/cloud/atlas
- Ücretsiz tier kullan
- Connection string'i kopyala
- .env'ye yapıştır

---

## 📊 Gerekli Data Dosyaları

### KRİTİK (Olmadan çalışmaz):

```
backend\data\
├── embeddings\
│   ├── mpnet_768d.npy              (~200 MB) ✅ ZORUNLU
│   └── clip_image_768d_normalized.npy (~500 MB) ✅ ZORUNLU
├── meta_ssot.csv                   (11.5 MB) ✅ ZORUNLU
└── product_attributes.csv          (14.6 MB) ⚠️ Önemli
```

**copy_data.bat** bu dosyaları otomatik kopyalar!

---

## ✅ Backend Kurulumu (Detaylı)

### 1. Data Dosyalarını Kopyala

```cmd
cd backend
copy_data.bat
```

Eski proje yolunu gir:
```
Örnek: C:\Users\LENOVO\Downloads\ai-fashion-complete\backend
```

### 2. Setup Çalıştır

```cmd
setup_backend.bat
```

Bu script:
- ✅ Python venv oluşturur
- ✅ Dependencies yükler (5-10 dakika)
- ✅ .env dosyası oluşturur

### 3. .env Dosyasını Düzenle

`.env` dosyası otomatik açılır. Şunları doldur:

```env
# MongoDB (Seç birini)
MONGODB_URL=mongodb://localhost:27017
# veya
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/ai_fashion_db

# JWT Secret (Rastgele güçlü bir key)
SECRET_KEY=super-guclu-rastgele-bir-anahtar-buraya

# GROQ API Key (Chat için)
GROQ_API_KEY=gsk_...buraya-groq-api-key
```

**GROQ API Key nasıl alınır:**
1. https://console.groq.com/
2. Ücretsiz hesap oluştur
3. API Keys → Create New Key

### 4. MongoDB'yi Başlat

**Yerel MongoDB:**
```cmd
services.msc
→ MongoDB Server'ı bul
→ Start
```

**Atlas:** Zaten çalışıyor, hiçbir şey yapma!

### 5. Backend'i Çalıştır

```cmd
run_backend.bat
```

**Başarılı çıktı:**
```
✅ Connected to MongoDB: ai_fashion_db
✅ Text model loaded (MPNet - 768d)
✅ CLIP model loaded (ViT-B/32 - 512d → padded to 768d)
✅ Products loaded: 44417
✅ Text index: 44417 vectors (768d)
✅ Image index: 44417 vectors (768d)
🎉 ML Loader ready!
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Test et:** http://localhost:8000/docs

---

## ✅ Frontend Kurulumu (Detaylı)

### 1. Setup Çalıştır

```cmd
cd frontend
setup_frontend.bat
```

Bu script:
- ✅ npm install yapar
- ✅ Dependencies yükler (2-3 dakika)

### 2. Frontend'i Çalıştır

```cmd
run_frontend.bat
```

**Tarayıcı otomatik açılır:** http://localhost:5173

---

## 🎯 Özellikler

### ✅ Search Fonksiyonları:
- 🔍 **Text Search** - MPNet semantic search with 768d embeddings
- 🖼️ **Image Search** - CLIP-powered visual similarity (ViT-B/32)
- 🎨 **Multimodal** - Combined text + image search
- ⭐ **Personalization** - Results boosted by user preferences

### ✅ AI Features:
- 💬 **Chat Assistant** - Llama-3.3-70B via GROQ
- 🤖 **Smart Recommendations** - Context-aware suggestions
- 📊 **Personalization Engine** - Learns from favorites and preferences
- 🌐 **Multilingual** - Supports Turkish and English

### ✅ User Features:
- 🔐 **Authentication** - JWT-based secure login
- ❤️ **Favorites** - Save and manage favorite products
- 👤 **Profile** - Customizable style preferences
- 🎨 **Style Settings** - Casual, Formal, Sportswear, etc.
- 📐 **Size Preferences** - XS to XXL
- 🌈 **Color Preferences** - Personalized color boosting
- 📝 **Search History** - Track your searches

### ✅ Technical Features:
- ⚡ **Fast Search** - ~100ms average response time
- 🔄 **Real-time Updates** - Live search results
- 📱 **Responsive Design** - Works on all screen sizes
- 🎨 **Modern UI** - Clean, intuitive interface
- 🔒 **Secure** - JWT tokens, password hashing
- 🌐 **RESTful API** - FastAPI backend

### ✅ Düzeltilmiş Sorunlar:
- ✅ FAISS dimension mismatch (512d → 768d)
- ✅ Image search errors
- ✅ Multimodal FormData issues
- ✅ Favorites sync in chat
- ✅ Profile preferences persistence
- ✅ PyMongo/Motor compatibility
- ✅ NumPy 2.x issues

---

## 🆘 Sorun Giderme

### "Python bulunamadı"
**Çözüm:**
1. Python'u yükle: https://www.python.org/downloads/
2. ⚠️ "Add to PATH" işaretle
3. Terminali kapat ve yeniden aç
4. Test: `python --version`

### "MongoDB bağlanamıyor"
**Çözüm 1 (Yerel):**
```cmd
services.msc
→ MongoDB Server
→ Start
```

**Çözüm 2 (Atlas):**
```env
# .env dosyasında
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/ai_fashion_db
```

### "ML models not loaded"
**Çözüm:**
```cmd
# Data dosyalarını kontrol et
dir backend\data\embeddings\*.npy
dir backend\data\*.csv

# Yoksa copy_data.bat'ı tekrar çalıştır
```

### "AssertionError: d == index.d"
**Bu versiyon FİXLENDİ!** CLIP 512d → 768d padding otomatik yapılıyor.

### "npm install" hatası
**Çözüm:**
```cmd
cd frontend

# Cache temizle
npm cache clean --force

# node_modules sil
rmdir /s /q node_modules
del package-lock.json

# Yeniden yükle
npm install --legacy-peer-deps
```

### "Port 8000 kullanımda"
**Çözüm:**
```cmd
# Port'u kullanan programı bul
netstat -ano | findstr :8000

# PID'yi not et, sonra:
taskkill /PID 1234 /F
```

### "PyMongo/Motor uyumsuzluk"
**Çözüm:**
```cmd
cd backend
fix_dependencies.bat
```

### "NumPy 2.x hatası"
**Çözüm:**
```cmd
cd backend
venv\Scripts\activate.bat
pip uninstall -y numpy
pip install "numpy<2"
```

---

## 📂 Klasör Yapısı

```
ai-fashion-WINDOWS/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/
│   │   │   ├── search_updated.py  ✅ Fixed
│   │   │   ├── users_updated.py   ✅ Fixed
│   │   │   ├── chat_updated.py    ✅ Multilingual
│   │   │   └── auth.py
│   │   ├── core/
│   │   │   ├── ml_loader.py       ✅ 768d support
│   │   │   ├── personalization.py ✅ Preference boosting
│   │   │   └── config.py
│   │   ├── services/
│   │   │   ├── search_engine.py   ✅ CLIP padding
│   │   │   ├── rag_service.py     ✅ Chat context
│   │   │   └── multimodal_retriever.py
│   │   └── middleware/
│   ├── data/                      ⚠️ Eski projeden kopyala
│   ├── main.py
│   ├── requirements.txt           ✅ Fixed versions
│   ├── setup_backend.bat
│   ├── run_backend.bat
│   ├── fix_dependencies.bat
│   └── copy_data.bat
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── SearchPage.jsx     ✅ Fixed
│   │   │   ├── ChatPage.jsx       ✅ Fixed
│   │   │   ├── ProfilePage.jsx    ✅ Fixed
│   │   │   ├── FavoritesPage.jsx  ✅ Sync working
│   │   │   ├── LoginPage.jsx
│   │   │   └── RegisterPage.jsx
│   │   ├── services/api.js
│   │   └── contexts/AuthContext.jsx
│   ├── setup_frontend.bat
│   └── run_frontend.bat
├── screenshots/                   📸 Application screenshots
└── README.md
```

---

## 🔧 Teknolojiler

### Backend:
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database
- **FAISS** - Vector similarity search (Facebook AI)
- **CLIP** - Image understanding (OpenAI ViT-B/32)
- **MPNet** - Text embeddings (768d)
- **GROQ** - Fast LLM inference (Llama-3.3-70B)
- **JWT** - Secure authentication
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation

### Frontend:
- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Navigation
- **Axios** - HTTP client
- **Lucide React** - Icons
- **CSS3** - Modern styling

### ML/AI:
- **Sentence Transformers** - Text embeddings
- **OpenAI CLIP** - Image embeddings
- **FAISS** - Efficient similarity search
- **LangChain** - LLM orchestration
- **GROQ** - Llama-3.3-70B inference

---

## 📊 Performans

- **Products:** 44,417
- **Embedding Dimension:** 768d (both text and image)
- **Text Search Time:** ~50-100ms
- **Image Search Time:** ~100-150ms
- **Chat Response:** ~1-2s
- **Index Size:** ~1.7 GB
- **Total with Images:** ~4-7 GB

---

## 🚀 Production Deployment

### Backend:
1. Güçlü SECRET_KEY kullan (minimum 32 chars)
2. MongoDB Atlas kullan (production cluster)
3. HTTPS enable et
4. CORS düzgün yapılandır
5. Rate limiting ekle
6. Environment variables'ı güvenli tut
7. Logging ekle
8. Monitoring kur (Sentry, DataDog, etc.)

### Frontend:
```cmd
cd frontend
npm run build
```

Deploy seçenekleri:
- **Vercel** - Recommended for React apps
- **Netlify** - Easy deployment
- **AWS S3 + CloudFront** - Scalable
- **Azure Static Web Apps** - Microsoft stack
- **GitHub Pages** - Free for public repos

---

## 📞 Yardım

### Log Dosyaları:
- **Backend:** Terminal çıktısı
- **Frontend:** Browser Console (F12)
- **MongoDB:** `C:\Program Files\MongoDB\Server\6.0\log\`

### Sık Hatalar:

| Hata | Çözüm |
|------|-------|
| Python bulunamadı | PATH'e ekle |
| MongoDB error | services.msc'de başlat |
| npm install error | `--legacy-peer-deps` |
| Port kullanımda | `taskkill /PID xxx /F` |
| ML models hata | copy_data.bat |
| GROQ API error | API key kontrol et |
| JWT error | SECRET_KEY kontrol et |

---

## 📝 Notlar

### Ports:
- Backend: **8000**
- Frontend: **5173**
- MongoDB: **27017**

### Data Size:
- Text embeddings: **~200 MB**
- Image embeddings: **~500 MB**
- Product data: **~26 MB**
- Total: **~726 MB** (minimum)
- With images: **~4-7 GB**

### API Limits:
- GROQ Free Tier: 14,400 requests/day
- MongoDB Atlas Free: 512 MB storage

---

## ✅ Test Checklist

### Backend:
- [ ] http://localhost:8000/docs açılıyor
- [ ] MongoDB bağlantısı çalışıyor
- [ ] ML models yükleniyor (44417 products)
- [ ] Text search çalışıyor
- [ ] Image search çalışıyor
- [ ] Multimodal search çalışıyor
- [ ] Chat endpoint çalışıyor

### Frontend:
- [ ] http://localhost:5173 açılıyor
- [ ] Kayıt olabiliyorum
- [ ] Giriş yapabiliyorum
- [ ] Text search sonuç veriyor
- [ ] Image search çalışıyor
- [ ] Multimodal search çalışıyor
- [ ] Chat çalışıyor
- [ ] Favorites ekleniyor
- [ ] Profile kaydediliyor
- [ ] Personalization aktif

---

## 🎓 Learning Resources

### For Developers:
- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/
- **FAISS:** https://github.com/facebookresearch/faiss
- **CLIP:** https://github.com/openai/CLIP
- **LangChain:** https://python.langchain.com/

### For Users:
- **GROQ Console:** https://console.groq.com/
- **MongoDB Atlas:** https://www.mongodb.com/cloud/atlas
- **Vector Search Basics:** Understanding embeddings and similarity

---

## 🤝 Contributing

Bu proje kişisel bir eğitim projesidir. Önerileriniz için issue açabilirsiniz.

---

## 📄 License

MIT License - Educational purposes

---

## 🙏 Acknowledgments

- **OpenAI** - CLIP model
- **Facebook AI** - FAISS library
- **HuggingFace** - Sentence Transformers
- **GROQ** - Fast LLM inference
- **Anthropic** - Claude AI assistance

---

**Version:** 3.0 Final - Windows Optimized  
**Status:** Production Ready ✅  
**Date:** January 2026  
**All Features:** Fully Functional 🎉  
**Dataset:** 44,417 Fashion Products

---

## 📸 Screenshot Index

All screenshots are available in the `screenshots/` directory:

1. `Anasayfa.jpg` - Landing page (logged out)
2. `Anasayfa2.jpg` - Home page (logged in, personalized)
3. `LoginPage.jpg` - Login interface
4. `CreateAccount.jpg` - Registration page
5. `SearchPage.jpg` - Search interface
6. `TextSearchWithResults.jpg` - Text search results
7. `İmageSearch.jpg` - Image search upload
8. `İmageSearchResults.jpg` - Image search results
9. `MultimodalSearch.jpg` - Multimodal search (text + image)
10. `ChatbotTC.jpg` - AI chat (Turkish)
11. `Ekran_AlıntısıChatbot.PNG` - AI chat (English)
12. `Favorites.jpg` - Favorites page
13. `Profile.jpg` - User profile and preferences

---

**⭐ Projeyi beğendiyseniz yıldızlamayı unutmayın!**
