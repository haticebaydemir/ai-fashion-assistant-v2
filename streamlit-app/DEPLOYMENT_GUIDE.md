# Hugging Face Deployment Guide

## 📋 Adım Adım Kurulum

### 1. Hugging Face Dataset Oluştur

1. **https://huggingface.co** → Login
2. **New Dataset** → Name: `fashion-assistant-data`
3. **Upload Files:**
   - `meta_ssot.csv` (Google Drive'dan)
   - `mpnet_768d.npy` (Google Drive'dan)
4. **Make Public** ✅

---

### 2. Username'i Güncelle

**`utils_search.py` dosyasında değiştir:**

```python
# Satır 28-29 civarı:
repo_id="YOUR_USERNAME/fashion-assistant-data",  # ← Buraya senin username'ini yaz
```

**Örnek:**
```python
repo_id="hatice-baydemir/fashion-assistant-data",
```

---

### 3. GitHub'a Upload Et

**Dosya yapısı:**
```
ai_fashion_assistant_v2/
└── v2.5-user-study/
    └── streamlit-app/
        ├── .streamlit/
        │   └── config.toml
        ├── app.py
        ├── streamlit_app.py
        ├── utils_search.py  ← USERNAME DEĞİŞTİR!
        ├── page_demo.py
        ├── page_study.py
        ├── page_about.py
        ├── requirements.txt
        ├── .gitignore
        └── README.md
```

**GitHub'a commit:**
```bash
git add v2.5-user-study/streamlit-app/
git commit -m "Add Streamlit app for user study"
git push origin main
```

---

### 4. Hugging Face Space Oluştur

1. **https://huggingface.co** → **New Space**
2. **Name:** `ai-fashion-assistant-v25`
3. **SDK:** Streamlit
4. **Hardware:** CPU basic (free)
5. **Visibility:** Public
6. **Create Space**

---

### 5. GitHub'ı Bağla

**Space Settings → Repository:**

- **Source repository:** `https://github.com/YOUR_USERNAME/ai_fashion_assistant_v2`
- **Subdirectory:** `v2.5-user-study/streamlit-app/`
- **Branch:** `main`
- **Auto-sync:** ✅ On
- **Save**

---

### 6. Build & Deploy

- ⏳ Building... (~5-10 dakika)
- ✅ Running!

**URL:**
```
https://huggingface.co/spaces/YOUR_USERNAME/ai-fashion-assistant-v25
```

---

## 🎯 Test

1. URL'i aç
2. Participant ID: `P001`
3. User Study → Task 1 dene
4. ✅ Çalışıyor!

---

## 🐛 Sorun Giderme

### Hata: "Cannot load data"

**Çözüm:** `utils_search.py`'de username'i kontrol et

### Hata: "Model download slow"

**Normal:** İlk çalıştırmada 5-10 dk sürer

### Hata: "Space build failed"

**Kontrol et:**
- ✅ Dataset public mi?
- ✅ Username doğru mu?
- ✅ Dosyalar doğru yerde mi?

---

## ✅ Tamamlandı!

Kalıcı URL ile user study başlayabilir! 🎉
