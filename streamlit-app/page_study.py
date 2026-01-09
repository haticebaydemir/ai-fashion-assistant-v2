"""
User Study Page
5 Evaluation Tasks
"""

import streamlit as st
from utils_search import search_products, get_product_image
import json
from pathlib import Path
from datetime import datetime
import os

st.title("📊 User Study - Evaluation Tasks")

# Check if logged in
if st.session_state.participant_id == "GUEST":
    st.error("❌ User study requires a valid Participant ID")
    st.info("Please go back to Home and login with your Participant ID (e.g., P001)")
    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        st.rerun()
    st.stop()

st.success(f"✅ Participant: **{st.session_state.participant_id}**")

# Initialize task state
if 'current_task' not in st.session_state:
    st.session_state.current_task = 1
if 'task_queries' not in st.session_state:
    st.session_state.task_queries = {}
if 'task_completed' not in st.session_state:
    st.session_state.task_completed = set()

# Task definitions
TASKS = {
    1: {
        'title': 'Find a white formal shirt for office wear',
        'description': 'Search for a formal white shirt suitable for professional office environment.',
        'hint': 'Try: "white formal shirt office"'
    },
    2: {
        'title': 'Find blue casual jeans for weekend',
        'description': 'Look for comfortable casual jeans in blue color for weekend wear.',
        'hint': 'Try: "blue casual jeans weekend"'
    },
    3: {
        'title': 'Find something for a summer wedding',
        'description': 'Search for elegant attire appropriate for a summer wedding event.',
        'hint': 'Try: "elegant summer wedding dress" or "summer wedding outfit"'
    },
    4: {
        'title': 'Refine your previous search',
        'description': 'Now search for the same items but in a different color (e.g., if you searched for blue, try red).',
        'hint': 'Modify the color in your previous query'
    },
    5: {
        'title': 'Find casual comfortable sneakers for walking',
        'description': 'Look for comfortable sneakers suitable for casual walking.',
        'hint': 'Try: "casual comfortable sneakers walking"'
    }
}

# Progress bar
progress = len(st.session_state.task_completed) / len(TASKS)
st.progress(progress, text=f"Progress: {len(st.session_state.task_completed)}/{len(TASKS)} tasks completed")

st.markdown("---")

# Task navigation
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    if st.session_state.current_task > 1:
        if st.button("⬅️ Previous"):
            st.session_state.current_task -= 1
            st.rerun()

with col2:
    st.markdown(f"### Task {st.session_state.current_task} of {len(TASKS)}")

with col3:
    if st.session_state.current_task < len(TASKS):
        if st.button("Next ➡️"):
            st.session_state.current_task += 1
            st.rerun()

# Current task
current_task = TASKS[st.session_state.current_task]

st.markdown(f"## 🎯 {current_task['title']}")
st.info(current_task['description'])

with st.expander("💡 Hint", expanded=False):
    st.markdown(current_task['hint'])

st.markdown("---")

# Search interface
query_key = f"task_{st.session_state.current_task}_query"
query = st.text_input(
    "🔍 Enter your search query:",
    key=query_key,
    value=st.session_state.task_queries.get(st.session_state.current_task, "")
)

col_search, col_mark = st.columns([3, 1])

with col_search:
    search_button = st.button("Search", type="primary", use_container_width=True)

with col_mark:
    if st.session_state.current_task not in st.session_state.task_completed:
        if st.button("✅ Mark Complete", use_container_width=True):
            st.session_state.task_completed.add(st.session_state.current_task)
            st.session_state.task_queries[st.session_state.current_task] = query
            
            # Log completion
            log_dir = Path('logs')
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / f'task_{st.session_state.participant_id}_task{st.session_state.current_task}.json'
            
            with open(log_file, 'w') as f:
                json.dump({
                    'participant_id': st.session_state.participant_id,
                    'task_number': st.session_state.current_task,
                    'query': query,
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
            
            st.success("✅ Task marked as complete!")
            st.rerun()
    else:
        st.success("✅ Completed")

st.markdown("---")

# Search results
if query and search_button:
    with st.spinner("🔍 Searching..."):
        results = search_products(query, k=10)
    
    if results:
        st.success(f"✅ Found {len(results)} results")
        
        # Display results
        for i, product in enumerate(results, 1):
            col_img, col_info = st.columns([1, 3])
            
            with col_img:
                image_path = get_product_image(product['id'])
                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/150x150.png?text=No+Image", 
                            use_container_width=True)
            
            with col_info:
                st.markdown(f"**{i}. {product['name']}**")
                st.caption(f"{product['category']} | {product['color']} | {product['gender']}")
                st.caption(f"Score: {product['score']:.4f}")
            
            st.divider()
    else:
        st.error("❌ No results found. Try a different query!")

# Completion check
if len(st.session_state.task_completed) == len(TASKS):
    st.markdown("---")
    st.success("🎉 **All tasks completed!**")
    
    st.markdown("### 📝 Next Step: Questionnaire")
    st.info("Please fill out the evaluation questionnaire to complete the study.")
    
    FORMS_LINK = "https://forms.gle/Bu5RNjedJ9HD1B6G7"
    
    st.markdown(f"""
    <a href="{FORMS_LINK}" target="_blank">
        <button style="
            background-color: #4CAF50;
            color: white;
            padding: 15px 32px;
            text-align: center;
            font-size: 18px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            width: 100%;
        ">
            📝 Open Questionnaire
        </button>
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown(f"1. Click the button above to open the questionnaire")
    st.markdown(f"2. Enter your Participant ID: **{st.session_state.participant_id}**")
    st.markdown(f"3. Answer all questions (SUS + Custom)")
    st.markdown(f"4. Submit the form")
    
    st.balloons()

# Task summary sidebar
with st.sidebar:
    st.markdown("### 📋 Task Summary")
    for task_num in range(1, len(TASKS) + 1):
        status = "✅" if task_num in st.session_state.task_completed else "⏳"
        st.markdown(f"{status} Task {task_num}")
    
    st.markdown("---")
    completion_pct = len(st.session_state.task_completed) / len(TASKS) * 100
    st.metric("Completion", f"{completion_pct:.0f}%")
