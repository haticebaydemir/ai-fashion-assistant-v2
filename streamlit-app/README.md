# AI Fashion Assistant v2.4.5 - Streamlit App

**User Study Interface + Production Demo**

---

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run streamlit_app.py
```

App will open at: `http://localhost:8501`

---

### Google Colab Deployment

```python
# 1. Upload files to Google Drive
# 2. Mount Drive in Colab
from google.colab import drive
drive.mount('/content/drive')

# 3. Navigate to project directory
import os
os.chdir('/content/drive/MyDrive/ai_fashion_assistant_v2')

# 4. Install dependencies
!pip install -q streamlit sentence-transformers faiss-cpu

# 5. Run Streamlit with ngrok tunnel
!streamlit run streamlit_app.py & npx localtunnel --port 8501
```

---

## 📁 File Structure

```
streamlit-app/
├── streamlit_app.py          # Main app (login, navigation)
├── page_demo.py               # Demo search interface
├── page_study.py              # User study tasks
├── page_about.py              # Project information
├── utils_search.py            # Search utilities
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

---

## 🎯 Features

### 1. **Home Page**
- Participant login (P001-P025)
- Guest access for demo
- Navigation menu

### 2. **Demo Search** 🔍
- Free exploration
- Real-time search
- Product images & details
- Multimodal v2.4.5 system

### 3. **User Study** 📊
- 5 evaluation tasks
- Progress tracking
- Query logging
- Form redirect

### 4. **About** ℹ️
- Project overview
- Technology stack
- Performance metrics
- Research contributions

---

## 🔧 Configuration

### Update Paths

In `utils_search.py`, update these paths:

```python
products_df = pd.read_csv('YOUR_PATH/data/processed/meta_ssot.csv')
text_embeddings = np.load('YOUR_PATH/v2.0-baseline/embeddings/text/mpnet_768d.npy')
```

### Update Form Link

In `page_study.py`:

```python
FORMS_LINK = "YOUR_GOOGLE_FORMS_LINK"
```

---

## 📊 Data Requirements

App needs access to:
- ✅ `data/processed/meta_ssot.csv` (product metadata)
- ✅ `v2.0-baseline/embeddings/text/mpnet_768d.npy` (embeddings)
- ✅ `data/images/` (product images - optional)

---

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub repo
4. Deploy!

**Pros:** Free, easy, public URL

### Option 2: Ngrok (Quick testing)

```bash
# Install ngrok
pip install pyngrok

# Run in Python
from pyngrok import ngrok
import subprocess

# Start Streamlit
subprocess.Popen(["streamlit", "run", "streamlit_app.py"])

# Create tunnel
public_url = ngrok.connect(8501)
print(f"Public URL: {public_url}")
```

**Pros:** Instant public URL

### Option 3: Hugging Face Spaces

1. Create new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Upload files
3. Add `requirements.txt`
4. Auto-deployed!

**Pros:** Free, persistent, ML-friendly

---

## 👥 User Study Usage

### For Researchers:

1. **Deploy app** (Streamlit Cloud / Ngrok)
2. **Share link** with participants
3. **Participants:**
   - Login with ID (P001-P025)
   - Complete 5 tasks
   - Fill questionnaire
4. **Collect data:**
   - Google Forms responses
   - Session logs in `logs/`

### For Participants:

1. Open the link
2. Enter Participant ID (e.g., P001)
3. Go to "User Study"
4. Complete 5 tasks (~10 min)
5. Fill questionnaire
6. Done! 🎉

---

## 📝 Session Logging

App automatically logs:
- Participant ID
- Task queries
- Timestamps
- Session events

**Log files:** `logs/session_P001_*.json`

---

## 🐛 Troubleshooting

### Error: "Cannot load data"

**Solution:** Update paths in `utils_search.py`

### Error: "Model download failed"

**Solution:** 
```bash
# Pre-download models
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')"
```

### Images not showing

**Solution:** Images are optional. App works without them (placeholder shown)

---

## 🎨 Customization

### Change Theme

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Update Logo

Replace logo URL in `streamlit_app.py`:

```python
st.image("YOUR_LOGO_URL", width=150)
```

---

## 📧 Support

**Issues?** Contact:
- Student: Hatice Baydemir
- Advisor: İlya Kuş
- Institution: Karamanoğlu Mehmetbey University

---

## 📄 License

MIT License - TÜBİTAK 2209-A Project

---

**Version:** 2.5  
**Last Updated:** January 2026  
**Status:** Production Ready ✅
