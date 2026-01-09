"""
About Page
Project information and technology details
"""

import streamlit as st

st.title("ℹ️ About AI Fashion Assistant")

st.markdown("---")

# Project Overview
st.markdown("## 📋 Project Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Program:** TÜBİTAK 2209-A Undergraduate Research Projects Support Program
    
    **Duration:** September 2025 - February 2026
    
    **Student Researcher:** Hatice Baydemir
    
    **Advisor:** İlya Kuş
    
    **Institution:** Karamanoğlu Mehmetbey University
    """)

with col2:
    st.markdown("""
    **Current Version:** v2.4.5 (Multimodal RAG)
    
    **Dataset:** 44,417 fashion products
    
    **Performance:** 97.4% NDCG@10
    
    **Features:** Multimodal search, Visual RAG, Personalization
    """)

st.markdown("---")

# System Evolution
st.markdown("## 🚀 System Evolution")

timeline_data = [
    ("v2.0", "September-December 2025", "Baseline System", "97.4% NDCG@10, Text-only search"),
    ("v2.1", "January 1, 2026", "Visual Attributes", "307K attributes, 10 categories"),
    ("v2.2", "January 2, 2026", "RAG Pipeline", "0.89s response time, LLM integration"),
    ("v2.3", "January 3-4, 2026", "AI Agents", "100% tool usage, Conversational AI"),
    ("v2.4", "January 5, 2026", "Personalization", "76.7% preference match, <12ms latency"),
    ("v2.4.5", "January 6-12, 2026", "Multimodal RAG", "Image query support, 7.6 visual keywords"),
]

for version, date, feature, metrics in timeline_data:
    with st.expander(f"**{version}** - {feature} ({date})"):
        st.markdown(f"**Key Metrics:** {metrics}")

st.markdown("---")

# Technology Stack
st.markdown("## 🛠️ Technology Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🤖 AI/ML")
    st.markdown("""
    - CLIP (OpenAI)
    - Sentence Transformers
    - GROQ LLama-3.3-70B
    - LangChain
    - PyTorch
    """)

with col2:
    st.markdown("### 🔍 Search")
    st.markdown("""
    - FAISS (Facebook AI)
    - Vector embeddings
    - Multimodal fusion
    - Semantic search
    - Visual attributes
    """)

with col3:
    st.markdown("### 💻 Development")
    st.markdown("""
    - Python 3.10+
    - Streamlit
    - Pandas/NumPy
    - FastAPI
    - Docker
    """)

st.markdown("---")

# Key Features
st.markdown("## ✨ Key Features")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("### 🔍 Search Capabilities")
    st.markdown("""
    - **Text Search:** Natural language queries
    - **Image Search:** Search with product images
    - **Multimodal Fusion:** Combined text + image
    - **Visual Awareness:** 307K extracted attributes
    - **Fast Response:** <1s average
    """)

with feature_col2:
    st.markdown("### 🤖 AI Features")
    st.markdown("""
    - **RAG System:** Retrieval-Augmented Generation
    - **Visual RAG:** Attribute-aware responses
    - **AI Agents:** Conversational interface
    - **Personalization:** User preference learning
    - **Multilingual:** Turkish + English support
    """)

st.markdown("---")

# Performance Metrics
st.markdown("## 📊 Performance Metrics")

metrics_data = {
    "Retrieval Quality": [
        ("NDCG@10", "97.43%", "Near-perfect ranking"),
        ("MRR", "100%", "Perfect first-rank accuracy"),
        ("Recall@10", "51.1%", "Effective large-scale retrieval"),
    ],
    "System Performance": [
        ("Response Time (v2.2)", "0.89s", "Sub-second RAG"),
        ("Personalization (v2.4)", "11.92ms", "Real-time matching"),
        ("Visual Awareness (v2.4.5)", "7.6 keywords", "Per response"),
    ],
    "User Evaluation": [
        ("Test Queries", "104", "Bilingual evaluation"),
        ("Visual Attributes", "307K", "CLIP zero-shot"),
        ("Target SUS Score", ">70", "Good usability"),
    ]
}

for category, metrics in metrics_data.items():
    st.markdown(f"### {category}")
    cols = st.columns(3)
    for i, (metric, value, desc) in enumerate(metrics):
        with cols[i]:
            st.metric(metric, value, desc)

st.markdown("---")

# Research Contributions
st.markdown("## 🎓 Research Contributions")

st.markdown("""
1. **Novel Multimodal Fusion**
   - Learned fusion of semantic and visual embeddings
   - Optimal weighting (α=0.7) validated empirically

2. **Visual Attribute Extraction**
   - 307K attributes via CLIP zero-shot classification
   - 10 semantic categories with 95.4% coverage

3. **Production RAG System**
   - Framework-agnostic implementation
   - Sub-second response with high quality (0.714 avg score)

4. **Conversational AI Integration**
   - ReAct-style agents with specialized tools
   - 100% success rate, 100% tool usage

5. **User-Centric Personalization**
   - Multi-strategy content-based filtering
   - Real-time matching with <12ms latency

6. **Multimodal RAG Innovation**
   - Image query support with visual-aware generation
   - Attribute-enhanced prompting for better responses
""")

st.markdown("---")

# Dataset
st.markdown("## 📦 Dataset")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    **Source:** [Fashion Product Images Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)
    
    **Description:** Large-scale fashion e-commerce dataset with product images and metadata
    
    **Citation:** Param Aggarwal, Kaggle (2019)
    """)

with col2:
    st.metric("Total Products", "44,417")
    st.metric("Categories", "45")
    st.metric("Attributes", "307K+")

st.markdown("---")

# Contact
st.markdown("## 📧 Contact")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Student Researcher**
    
    Hatice Baydemir  
    Computer Science Department  
    Karamanoğlu Mehmetbey University
    """)

with col2:
    st.markdown("""
    **Academic Advisor**
    
    İlya Kuş  
    Karamanoğlu Mehmetbey University
    """)

st.markdown("---")

# Footer
st.markdown("### 🏆 Acknowledgments")
st.markdown("""
- **TÜBİTAK** for funding through the 2209-A program
- **Karamanoğlu Mehmetbey University** for institutional support
- **Open Source Community** for ML/AI tools and frameworks
""")

st.success("Thank you for your interest in the AI Fashion Assistant project!")
