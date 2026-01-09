"""
Demo Search Page
Free exploration of v2.4.5 system
"""

import streamlit as st
from utils_search import search_products, format_product_card, get_product_image
from pathlib import Path
import os

st.title("🔍 Demo Search")
st.markdown("Try the AI Fashion Assistant with your own queries!")

# Instructions
with st.expander("ℹ️ How to use", expanded=False):
    st.markdown("""
    **Try these example queries:**
    - "white formal shirt for office"
    - "blue casual jeans for weekend"
    - "elegant summer wedding dress"
    - "comfortable running shoes"
    - "vintage leather jacket"
    
    The system uses **multimodal AI** to understand your intent and find the best matches!
    """)

st.markdown("---")

# Search interface
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "🔍 Search for fashion products",
        placeholder="e.g., white formal shirt for office",
        key="demo_query"
    )

with col2:
    st.write("")  # Spacing
    st.write("")  # Spacing
    search_button = st.button("Search", type="primary", use_container_width=True)

# Number of results
num_results = st.slider("Number of results", 5, 20, 10)

st.markdown("---")

# Search results
if query and (search_button or st.session_state.get('last_query') != query):
    st.session_state.last_query = query
    
    with st.spinner("🔍 Searching..."):
        results = search_products(query, k=num_results)
    
    if results:
        st.success(f"✅ Found {len(results)} results for: **{query}**")
        
        st.markdown("### Results")
        
        # Display results in grid
        for i, product in enumerate(results, 1):
            col_img, col_info = st.columns([1, 3])
            
            with col_img:
                # Try to show image
                image_path = get_product_image(product['id'])
                if os.path.exists(image_path):
                    st.image(image_path, use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/200x200.png?text=No+Image", 
                            use_container_width=True)
            
            with col_info:
                st.markdown(f"### {i}. {product['name']}")
                
                # Details in columns
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.markdown(f"**Category:** {product['category']}")
                    st.markdown(f"**Color:** {product['color']}")
                    st.markdown(f"**Gender:** {product['gender']}")
                
                with detail_col2:
                    st.markdown(f"**Season:** {product['season']}")
                    st.markdown(f"**Usage:** {product['usage']}")
                    st.markdown(f"**Score:** {product['score']:.4f}")
            
            st.markdown("---")
    
    else:
        st.error("❌ No results found. Try a different query!")

elif not query:
    # Show placeholder
    st.info("👆 Enter a search query above to see results!")
    
    st.markdown("### 💡 Example Searches")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Formal Wear**
        - White formal shirt
        - Black suit jacket
        - Office trousers
        """)
    
    with col2:
        st.markdown("""
        **Casual Wear**
        - Blue jeans casual
        - Comfortable t-shirt
        - Weekend sneakers
        """)
    
    with col3:
        st.markdown("""
        **Special Occasions**
        - Summer wedding dress
        - Party outfit elegant
        - Festive ethnic wear
        """)

# Stats in sidebar
if query and results:
    with st.sidebar:
        st.markdown("### 📊 Search Stats")
        st.metric("Query Length", len(query.split()))
        st.metric("Results Found", len(results))
        st.metric("Avg Score", f"{sum(r['score'] for r in results)/len(results):.4f}")
