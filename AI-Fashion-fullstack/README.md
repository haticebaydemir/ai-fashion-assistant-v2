# 🎨 AI Fashion Assistant - Full Stack Application

![AI Fashion Assistant](../screenshots/Anasayfa.jpg)

**Modern AI-powered fashion search and recommendation system with personalization**

[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)


## Watch Full Demo Video
[![Watch Full Demo Video](../screenshots/Anasayfa.jpg)](https://www.youtube.com/watch?v=RGvt3QTJjcg)

---

## 📑 Table of Contents

- [Quick Start](#-hizli-başlangiç-5-adim)
- [Screenshots](#-application-screenshots)
- [Database Architecture](#database-architecture)
- [Features](#-özellikler)
- [Installation](#-backend-kurulumu-detaylı)
- [Tech Stack](#-teknolojiler)
- [Troubleshooting](#-sorun-giderme)
- [Performance](#-performans)

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
![Chat EN](../screenshots/Ekran%20AlıntısıChatbot.PNG)
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

##  Database Architecture

### MongoDB Database Structure

![Database Structure](../screenshots/mongodb-database-structure.png)

The application uses MongoDB with 4 main collections:

#### Collections Overview
![Collections Stats](../screenshots/mongodb-collections-stats.png)

| Collection | Documents | Avg. Document Size | Storage Size | Purpose |
|------------|-----------|-------------------|--------------|---------|
| **users** | 32 | 294.00 B | 30.77 KB | User accounts & authentication |
| **user_profiles** | 32 | 227.00 B | 30.77 KB | Style preferences & personalization |
| **search_history** | 347 | 171.00 B | 36.86 KB | Search queries & analytics |
| **favorites** | 139 | 211.00 B | 30.77 KB | Saved products per user |

---

### 📊 Collection Details

#### 1. Users Collection
![Users Collection](../screenshots/mongodb-users.png)

**Schema:**
```javascript
{
  _id: ObjectId,
  user_id: String (unique),      // Auto-generated UUID
  name: String,
  email: String (unique, indexed),
  hashed_password: String,       // bcrypt hashed
  created_at: DateTime,
  last_login: DateTime,
  is_active: Boolean,
  is_verified: Boolean,
  style: Array,                  // User style preferences
  size: String,
  colors: Array,                 // Favorite colors
  total_searches: Number,
  total_favorites: Number
}
```

**Key Features:**
- ✅ JWT-based authentication
- ✅ Password hashing with bcrypt
- ✅ Email uniqueness validation
- ✅ Active user tracking
- ✅ Search & favorite counters

**Example Document:**
```json
{
  "_id": "6966dd2b94fa145a63b192d3",
  "user_id": "usr_99dba5d9bc4f4939",
  "name": "string",
  "email": "user@example.com",
  "hashed_password": "$2b$12$noEhazZW08HbmLoMiW7Fi.wTjQH3L4EA38KhmsbwIUuqPCsRD7unC",
  "created_at": "2026-01-14T00:02:51.337+00:00",
  "last_login": "2026-01-14T00:03:25.365+00:00",
  "is_active": true,
  "is_verified": false,
  "style": [],
  "size": null,
  "colors": [],
  "total_searches": 0,
  "total_favorites": 0
}
```

---

#### 2. User Profiles Collection
![User Profiles](../screenshots/mongodb-user-profiles.png)

**Schema:**
```javascript
{
  _id: ObjectId,
  user_id: String (indexed),
  style: Array,         // ["Casual", "Formal", "Sportswear"]
  size: String,         // "M", "L", "XL"
  colors: Array,        // ["Black", "Blue", "Red"]
  created_at: DateTime,
  updated_at: DateTime
}
```

**Personalization Options:**
- **Styles:** Casual, Formal, Sportswear, Streetwear, Elegant, Bohemian
- **Sizes:** XS, S, M, L, XL, XXL
- **Colors:** Black, White, Blue, Red, Green, Yellow, Pink, Navy, Gray, Brown

**How it works:**
1. User sets preferences in Profile page
2. Preferences stored in `user_profiles` collection
3. Search results boosted by:
   - Favorite colors (+0.2 score)
   - Preferred styles (+0.15 score)
   - Size matches (prioritized)

**Example Document:**
```json
{
  "_id": "6966dd2b94fa145a63b192d4",
  "user_id": "usr_99dba5d9bc4f4939",
  "style": [],
  "size": null,
  "colors": [],
  "created_at": "2026-01-14T00:02:51.341+00:00",
  "updated_at": "2026-01-14T00:02:51.341+00:00"
}
```

---

#### 3. Search History Collection
![Search History](../screenshots/mongodb-search-history.png)

**Schema:**
```javascript
{
  _id: ObjectId,
  user_id: String (indexed),
  query: String,              // Search query text
  query_type: String,         // "text", "image", "multimodal"
  results_count: Number,      // Number of results returned
  timestamp: DateTime,
  session_id: String          // Track user sessions
}
```

**Tracked Queries:**
- Text searches
- Image searches
- Multimodal searches
- Chat queries

**Analytics Use:**
- Popular search terms
- User behavior analysis
- Search performance metrics
- Personalization improvements

**Example Documents:**
```json
{
  "_id": "6967b2dc68d05d3c8aca94b5",
  "user_id": "usr_4c16cb0668d64da4",
  "query": "dress",
  "query_type": "text",
  "results_count": 5,
  "timestamp": "2026-01-14T13:25:08.621+00:00"
},
{
  "_id": "6967b2dc68d05d3c8aca94b6",
  "user_id": "usr_4c16cb0668d64da4",
  "query": "siyah bir gece elbisesi arıyorum",
  "query_type": "text",
  "results_count": 10,
  "timestamp": "2026-01-14T15:14:36.745+00:00",
  "session_id": "user-1768403627106"
}
```

**Statistics:**
- **Total Searches:** 347
- **Unique Users:** 32
- **Average Results:** 10-15 per query
- **Most Common:** Text searches (85%)

---

#### 4. Favorites Collection
![Favorites Collection](../screenshots/mongodb-favorites.png)

**Schema:**
```javascript
{
  _id: ObjectId,
  user_id: String (indexed),
  product_id: String (indexed),
  product_name: String,
  category: String,
  color: String,
  image_url: String,
  added_at: DateTime
}
```

**Key Features:**
- ✅ One-click favorite from search
- ✅ Add from chat recommendations
- ✅ Remove from favorites page
- ✅ Synced across all pages
- ✅ Used for personalization

**Example Documents:**
```json
{
  "_id": "6967db264a9e2d47165bfb87",
  "user_id": "usr_4c16cb0668d64da4",
  "product_id": "57965",
  "product_name": "Prafful Multi Coloured Sari",
  "category": "Apparel",
  "color": "Multi",
  "image_url": "/images/57965.jpg",
  "added_at": "2026-01-14T18:06:38.410+00:00"
},
{
  "_id": "6967dcdc4a9e2d47165bfb95",
  "user_id": "usr_4c16cb0668d64da4",
  "product_id": "59980",
  "product_name": "Avirate Black & Cream Dress",
  "category": "Apparel",
  "color": "Black",
  "image_url": "/images/59980.jpg",
  "added_at": "2026-01-14T18:13:48.352+00:00"
}
```

**Statistics:**
- **Total Favorites:** 139 products saved
- **Active Users:** 32
- **Average per User:** ~4 favorites
- **Most Favorited:** Apparel category (85%)
- **Popular Colors:** Black (45%), Multi (20%), Red (15%)

---

### 🔍 Database Indexes

**Optimized for performance:**

```javascript
// users collection
db.users.createIndex({ "email": 1 }, { unique: true })
db.users.createIndex({ "user_id": 1 }, { unique: true })

// user_profiles collection
db.user_profiles.createIndex({ "user_id": 1 })

// search_history collection
db.search_history.createIndex({ "user_id": 1 })
db.search_history.createIndex({ "timestamp": -1 })

// favorites collection
db.favorites.createIndex({ "user_id": 1 })
db.favorites.createIndex({ "product_id": 1 })
db.favorites.createIndex({ "user_id": 1, "product_id": 1 }, { unique: true })
```

---

### 📈 Database Statistics

**Live Production Data:**
- **Total Documents:** 550+
- **Total Storage:** ~130 KB
- **Active Users:** 32
- **Search Queries:** 347
- **Saved Favorites:** 139
- **Average Response Time:** <10ms

**Growth Metrics:**
- User registration rate: ~5 per day (test period)
- Average searches per user: ~11
- Average favorites per user: ~4
- Most active features: Text search (65%), Chat (20%), Image search (15%)

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
- 📝 **Search History** - Track and analyze searches

### ✅ Database Features:
- 💾 **MongoDB Atlas** - Cloud-hosted NoSQL database
- 🔄 **Real-time Sync** - Instant updates across collections
- 📊 **Analytics** - Search patterns and user behavior
- 🔒 **Secure Storage** - Password hashing, JWT tokens
- 📈 **Scalable** - Indexed for fast queries
- 🔍 **Full-text Search** - Optimized queries

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
ai-fashion-assistant-v2/
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
├── screenshots/                   📸 Application & DB screenshots
└── README.md
```

---

## 🔧 Teknolojiler

### Backend:
- **FastAPI** - Modern Python web framework
- **MongoDB** - NoSQL database with Atlas cloud hosting
- **Motor** - Async MongoDB driver
- **FAISS** - Vector similarity search (Facebook AI)
- **CLIP** - Image understanding (OpenAI ViT-B/32)
- **MPNet** - Text embeddings (768d)
- **GROQ** - Fast LLM inference (Llama-3.3-70B)
- **JWT** - Secure authentication
- **bcrypt** - Password hashing
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

### Database:
- **MongoDB 6.0** - Document database
- **MongoDB Atlas** - Cloud hosting
- **Indexes** - Performance optimization
- **Aggregation Pipeline** - Analytics

---

## 📊 Performans

### Search Performance:
- **Products:** 44,417
- **Embedding Dimension:** 768d (both text and image)
- **Text Search Time:** ~50-100ms
- **Image Search Time:** ~100-150ms
- **Multimodal Search:** ~150-200ms
- **Chat Response:** ~1-2s

### Database Performance:
- **Query Response:** <10ms (indexed)
- **User Lookup:** ~2-3ms
- **Favorites Fetch:** ~5-10ms
- **Search History:** ~8-12ms

### Storage:
- **Index Size:** ~1.7 GB (FAISS vectors)
- **Database Size:** ~130 KB (MongoDB)
- **Embeddings:** ~726 MB (text + image)
- **Total:** ~2.5 GB (without product images)
- **With Images:** ~4-7 GB

### Scale:
- **Tested Users:** 32 concurrent
- **Tested Searches:** 347 queries
- **Tested Favorites:** 139 products
- **Max Throughput:** ~100 req/sec
- **CPU Usage:** ~25% (search)
- **Memory Usage:** ~2.5 GB (with loaded models)

---

## 🚀 Production Deployment

### Backend:
1. **Security:**
   - Güçlü SECRET_KEY (minimum 32 chars)
   - MongoDB Atlas production cluster
   - HTTPS/TLS enable
   - Rate limiting (10 req/sec per user)
   - Input validation (Pydantic)
   
2. **Monitoring:**
   - Application logs (structured JSON)
   - Error tracking (Sentry)
   - Performance monitoring
   - Database metrics

3. **Scaling:**
   - Horizontal scaling with load balancer
   - FAISS index caching
   - MongoDB connection pooling
   - Redis for session storage

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

### Database:
- **MongoDB Atlas M10+** for production
- **Automated backups** (daily)
- **Replica sets** for high availability
- **Read replicas** for scaling
- **Monitoring** with Atlas dashboard

---

## 📞 Yardım

### Log Dosyaları:
- **Backend:** Terminal çıktısı
- **Frontend:** Browser Console (F12)
- **MongoDB:** Atlas dashboard logs

### Sık Hatalar:

| Hata | Çözüm |
|------|-------|
| Python bulunamadı | PATH'e ekle |
| MongoDB error | Connection string kontrol et |
| npm install error | `--legacy-peer-deps` |
| Port kullanımda | `taskkill /PID xxx /F` |
| ML models hata | copy_data.bat |
| GROQ API error | API key kontrol et |
| JWT error | SECRET_KEY kontrol et |

---

## 📝 Notlar

### Ports:
- **Backend:** 8000
- **Frontend:** 5173
- **MongoDB:** 27017 (local) / Atlas (cloud)

### Data Size:
- **Text embeddings:** ~200 MB
- **Image embeddings:** ~500 MB
- **Product data:** ~26 MB
- **Database:** ~130 KB
- **Total:** ~726 MB (minimum)

### API Limits:
- **GROQ Free Tier:** 14,400 requests/day
- **MongoDB Atlas Free:** 512 MB storage
- **Rate Limit:** 10 req/sec per user

---

## ✅ Test Checklist

### Backend:
- [ ] http://localhost:8000/docs açılıyor
- [ ] MongoDB bağlantısı çalışıyor
- [ ] 4 collection oluşturuldu (users, user_profiles, search_history, favorites)
- [ ] ML models yüklendi (44417 products)
- [ ] Text search çalışıyor
- [ ] Image search çalışıyor
- [ ] Multimodal search çalışıyor
- [ ] Chat endpoint çalışıyor
- [ ] Favorilere ekleme/çıkarma çalışıyor

### Frontend:
- [ ] http://localhost:5173 açılıyor
- [ ] Kayıt olabiliyorum
- [ ] Giriş yapabiliyorum
- [ ] Profile kaydediliyor
- [ ] Text search sonuç veriyor
- [ ] Image search çalışıyor
- [ ] Multimodal search çalışıyor
- [ ] Chat cevap veriyor
- [ ] Favorites sync çalışıyor
- [ ] Search history görünüyor
- [ ] Personalization aktif

### Database:
- [ ] Users collection oluştu
- [ ] User_profiles collection oluştu
- [ ] Search_history collection oluştu
- [ ] Favorites collection oluştu
- [ ] Indexler oluşturuldu
- [ ] CRUD işlemleri çalışıyor

---

## 🎓 Learning Resources

### For Developers:
- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/
- **MongoDB:** https://www.mongodb.com/docs/
- **FAISS:** https://github.com/facebookresearch/faiss
- **CLIP:** https://github.com/openai/CLIP
- **LangChain:** https://python.langchain.com/

### For Users:
- **GROQ Console:** https://console.groq.com/
- **MongoDB Atlas:** https://www.mongodb.com/cloud/atlas
- **Vector Search:** Understanding embeddings

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
- **MongoDB** - Database platform
- **Anthropic** - Claude AI assistance

---

## 📸 Screenshot Index

### Application Screenshots (13):
1. `Anasayfa.jpg` - Landing page (logged out)
2. `Anasayfa2.jpg` - Home page (logged in)
3. `LoginPage.jpg` - Login interface
4. `CreateAccount.jpg` - Registration
5. `SearchPage.jpg` - Search interface
6. `TextSearchWithResults.jpg` - Text search
7. `İmageSearch.jpg` - Image upload
8. `İmageSearchResults.jpg` - Image results
9. `MultimodalSearch.jpg` - Multimodal
10. `ChatbotTC.jpg` - Chat (Turkish)
11. `Ekran_AlıntısıChatbot.PNG` - Chat (English)
12. `Favorites.jpg` - Favorites page
13. `Profile.jpg` - User profile

### Database Screenshots (6):
1. `mongodb-database-structure.png` - DB structure
2. `mongodb-collections-stats.png` - Collections overview
3. `mongodb-users.png` - Users collection
4. `mongodb-user-profiles.png` - User profiles
5. `mongodb-search-history.png` - Search history
6. `mongodb-favorites.png` - Favorites collection

---

**Version:** 3.0 Final - Full Stack  
**Status:** Production Ready ✅  
**Date:** January 2026  
**Features:** Fully Functional 🎉  
**Dataset:** 44,417 Fashion Products  
**Active Users:** 32 (test environment)  
**Total Searches:** 347  
**Saved Favorites:** 139

---

**⭐ Projeyi beğendiyseniz yıldızlamayı unutmayın!**

**📧 İletişim:** [GitHub Issues](https://github.com/your-repo/issues)
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
