# pages/5powerbi.py

import streamlit as st

st.set_page_config(layout="wide")
st.title("📊 Power BI Dashboard")

st.markdown("""
Welcome to the Power BI Insights page.

This page displays your embedded Power BI dashboard.  
If it doesn't load properly, make sure:
- The report is **published to web**
- The embed URL is **publicly accessible**

> 📌 Replace the placeholder URL below with your actual Power BI report link.
""")

# --- Embed URL Configuration ---
# You can also let user input the URL dynamically from sidebar or settings page
embed_url = "https://app.powerbi.com/view?r=YOUR_EMBED_CODE_HERE"

# --- Embed the Report ---
if "powerbi.com" not in embed_url or "YOUR_EMBED_CODE_HERE" in embed_url:
    st.error("❌ Please set a valid Power BI 'publish to web' embed URL.")
else:
    st.components.v1.iframe(embed_url, height=800, width="100%")
