# ⚡ QUICKSTART GUIDE - 5 DK'DA BAŞLA

## 🎯 3 KOMUT İLE ÇALIŞIR!

### Backend:
```cmd
cd backend
setup_backend.bat
run_backend.bat
```

### Frontend:
```cmd
cd frontend  
setup_frontend.bat
run_frontend.bat
```

**Aç:** http://localhost:5173

---

## ⚠️ ÖNEMLİ: İLK KURULUM

### 1. Data Dosyalarını Kopyala (İLK KEZ)

```cmd
cd backend
copy_data.bat
```

**Eski proje yolunu gir:**
```
C:\Users\LENOVO\Downloads\ai-fashion-complete\backend
```

**Bu dosyalar kopyalanacak:**
- `mpnet_768d.npy` (200 MB) ✅
- `clip_image_768d_normalized.npy` (500 MB) ✅
- `meta_ssot.csv` (11.5 MB) ✅
- `product_attributes.csv` (14.6 MB)

---

### 2. MongoDB Kur (İLK KEZ)

**Seçenek A: MongoDB Atlas (ÖNERİLEN)**

1. https://www.mongodb.com/cloud/atlas
2. Sign up (ücretsiz)
3. Create Cluster (M0 Free tier)
4. Get Connection String
5. `.env` dosyasına yapıştır:

```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/ai_fashion_db
```

**Seçenek B: Yerel MongoDB**

1. https://www.mongodb.com/try/download/community
2. İndir ve kur
3. services.msc → MongoDB Server → Start

---

### 3. .env Dosyasını Doldur

Backend klasöründe `.env` dosyası:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017  # veya Atlas URL

# JWT Secret
SECRET_KEY=rasgele-guclu-bir-anahtar-123456789

# GROQ API Key (Chat için)
GROQ_API_KEY=gsk_...buraya
```

**GROQ API Key al:**
1. https://console.groq.com/
2. Sign up
3. API Keys → Create New Key
4. Kopyala → `.env`'ye yapıştır

---

## ✅ Kurulum Başarılı mı Kontrol Et

### Backend Test:
```
✅ Connected to MongoDB: ai_fashion_db
✅ ML Loader ready!
✅ 44417 products loaded
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Tarayıcıda:** http://localhost:8000/docs

### Frontend Test:
```
VITE v... ready in ... ms
➜ Local: http://localhost:5173/
```

**Tarayıcıda:** http://localhost:5173

---

## 🆘 Hata Alırsan

### "Python bulunamadı"
```cmd
# Python yükle + ADD TO PATH
https://www.python.org/downloads/
```

### "MongoDB bağlanamıyor"
```cmd
services.msc → MongoDB Server → Start
# veya Atlas URL kullan
```

### "ML models not loaded"
```cmd
cd backend
copy_data.bat  # Tekrar çalıştır
```

### "npm install error"
```cmd
cd frontend
npm install --legacy-peer-deps
```

### "PyMongo hatası"
```cmd
cd backend
fix_dependencies.bat
```

---

## 🎯 İLK KULLANIM

1. **Kayıt Ol:** http://localhost:5173/register
2. **Giriş Yap:** Email + şifre
3. **Profile Doldur:** Style, colors, size seç
4. **Search Dene:** "black dress" ara
5. **Favorites Ekle:** ❤️ butonuna tıkla
6. **Chat Kullan:** "Show me casual dresses"

---

## 📊 Özellikler

✅ Text search  
✅ Image search  
✅ Multimodal search  
✅ AI chat assistant  
✅ Personalized results  
✅ Favorites  
✅ User profiles  
✅ Search history  

---

**Detaylı kılavuz:** README.md dosyasını oku!

**Version:** 3.0 Final  
**Status:** Production Ready ✅
