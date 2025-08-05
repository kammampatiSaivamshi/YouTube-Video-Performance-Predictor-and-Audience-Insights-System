# app.py

import streamlit as st

# Page config
st.set_page_config(
    page_title="YouTube Analytics and Insights",
    page_icon="📺",
    layout="wide",
)

# --- Big Centered YouTube Logo ---
st.markdown(
    """
    <div style='text-align: center; margin-bottom: 20px;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg' width='300'/>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Title and Intro ---
st.title("📺 YouTube Analytics and Insights")
st.markdown("""
Welcome to your interactive YouTube data analytics platform.

Use the **sidebar** to navigate through:
- 📊 **Video Performance Predictions**  
- 📈 **Visual Insights**  
- 💬 **Sentiment Analysis**  
- 🌍 **Geographic Insights**  
- ⚙️ **Settings & File Management**
""")

# --- Sidebar Guidance ---
st.sidebar.success("👈 Use the sidebar to explore each dashboard module.")

# --- Explore Modules Section ---
st.markdown("---")
st.subheader("✨ Explore Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 📊 Predictions")
    st.markdown("Forecast your video views using machine learning.")

with col2:
    st.markdown("#### 📈 Visual Insights")
    st.markdown("Interactive charts from your YouTube data.")

with col3:
    st.markdown("#### 💬 Sentiment Analysis")
    st.markdown("Understand audience feedback through NLP.")

col4, col5 = st.columns(2)

with col4:
    st.markdown("#### 🌍 Geo Insights")
    st.markdown("See where your viewers are coming from.")

with col5:
    st.markdown("#### ⚙️ Settings")
    st.markdown("Manage files and customize the dashboard.")

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
