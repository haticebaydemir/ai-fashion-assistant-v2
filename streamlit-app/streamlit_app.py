"""
AI Fashion Assistant v2.4.5 - Streamlit App
User Study Interface + Demo

TÜBİTAK 2209-A Project
Student: Hatice Baydemir
Version: 2.5
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# Page config
st.set_page_config(
    page_title="AI Fashion Assistant v2.4.5",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.2rem;
        padding: 0.75rem;
        border-radius: 10px;
    }
    .participant-badge {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'participant_id' not in st.session_state:
    st.session_state.participant_id = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=Fashion+AI", width=150)
    st.title("Navigation")
    
    if st.session_state.participant_id:
        st.markdown(f'<div class="participant-badge">👤 {st.session_state.participant_id}</div>', 
                   unsafe_allow_html=True)
        if st.button("🏠 Home"):
            st.session_state.page = 'home'
            st.rerun()
        if st.button("🔍 Demo Search"):
            st.session_state.page = 'demo'
            st.rerun()
        if st.button("📊 User Study"):
            st.session_state.page = 'study'
            st.rerun()
        if st.button("ℹ️ About"):
            st.session_state.page = 'about'
            st.rerun()
        if st.button("🚪 Logout"):
            st.session_state.participant_id = None
            st.session_state.page = 'home'
            st.rerun()
    else:
        st.info("Please login with your Participant ID")
    
    st.divider()
    st.caption("TÜBİTAK 2209-A Project")
    st.caption("Karamanoğlu Mehmetbey University")
    st.caption("v2.5 - January 2026")

# Main content
if st.session_state.page == 'home':
    # HOME PAGE
    st.markdown('<div class="main-header">👗 AI Fashion Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Multimodal Fashion Search with AI</div>', unsafe_allow_html=True)
    
    if not st.session_state.participant_id:
        st.markdown("---")
        st.subheader("🔐 Participant Login")
        st.info("**For User Study Participants:** Enter your Participant ID below")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            participant_id = st.text_input(
                "Participant ID",
                placeholder="e.g., P001",
                help="Your unique participant ID (format: P###)"
            )
            
            if st.button("Start Session", type="primary"):
                if participant_id and participant_id.startswith('P') and len(participant_id) == 4:
                    st.session_state.participant_id = participant_id
                    
                    # Log session start
                    log_dir = Path('logs')
                    log_dir.mkdir(exist_ok=True)
                    log_file = log_dir / f'session_{participant_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                    
                    log_data = {
                        'participant_id': participant_id,
                        'session_start': datetime.now().isoformat(),
                        'app_version': 'v2.4.5'
                    }
                    
                    with open(log_file, 'w') as f:
                        json.dump(log_data, f, indent=2)
                    
                    st.success(f"✅ Welcome, {participant_id}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid Participant ID format. Use P### (e.g., P001)")
        
        st.markdown("---")
        st.subheader("👀 Just Browsing?")
        st.info("You can explore the demo without logging in!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Try Demo Search"):
                st.session_state.participant_id = "GUEST"
                st.session_state.page = 'demo'
                st.rerun()
        with col2:
            if st.button("ℹ️ Learn More"):
                st.session_state.participant_id = "GUEST"
                st.session_state.page = 'about'
                st.rerun()
    
    else:
        # Logged in home
        st.success(f"✅ Logged in as: **{st.session_state.participant_id}**")
        
        st.markdown("---")
        st.subheader("📋 What would you like to do?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="feature-box">', unsafe_allow_html=True)
            st.markdown("### 🔍 Demo Search")
            st.write("Try the AI Fashion Assistant with your own queries")
            if st.button("Go to Demo", key="demo_btn"):
                st.session_state.page = 'demo'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="feature-box">', unsafe_allow_html=True)
            st.markdown("### 📊 User Study")
            st.write("Complete the 5 evaluation tasks (~10 minutes)")
            if st.button("Start Study", key="study_btn", type="primary"):
                st.session_state.page = 'study'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="feature-box">', unsafe_allow_html=True)
            st.markdown("### ℹ️ About")
            st.write("Learn about the project and technology")
            if st.button("Learn More", key="about_btn"):
                st.session_state.page = 'about'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'demo':
    st.markdown("🔍 **Demo Search** page will be implemented in next file...")
    st.info("This page will show the v2.4.5 search interface")

elif st.session_state.page == 'study':
    st.markdown("📊 **User Study** page will be implemented in next file...")
    st.info("This page will show the 5 evaluation tasks")

elif st.session_state.page == 'about':
    st.markdown("ℹ️ **About** page will be implemented in next file...")
    st.info("This page will show project information")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🎓 TÜBİTAK 2209-A")
with col2:
    st.caption("👩‍💻 Hatice Baydemir")
with col3:
    st.caption("🏛️ Karamanoğlu Mehmetbey Üniversitesi")
