# pages/6settings.py

import streamlit as st
import pandas as pd
import joblib
import os
import shutil

st.set_page_config(layout="wide")
st.title("⚙️ App Settings & File Management")

st.markdown("Use this page to upload new data files, update the model, or reset parts of the app.")

# --- Upload Data Files ---
st.subheader("📁 Upload Data Files")
uploaded_files = st.file_uploader(
    "Upload one or more CSV files (e.g., new video data, sentiment data, etc.)",
    type="csv",
    accept_multiple_files=True
)

if uploaded_files:
    os.makedirs("data", exist_ok=True)

    for file in uploaded_files:
        file_path = f"data/{file.name}"
        if os.path.exists(file_path):
            st.warning(f"⚠️ {file.name} already exists and will be overwritten.")
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        st.success(f"✅ Uploaded: {file.name}")

    if st.button("📄 Preview Uploaded Files"):
        for file in uploaded_files:
            st.markdown(f"**{file.name}**")
            try:
                df = pd.read_csv(f"data/{file.name}")
                st.dataframe(df.head())
            except Exception as e:
                st.error(f"❌ Could not read {file.name}: {e}")

st.divider()

# --- Upload Model ---
st.subheader("🧠 Upload New Model File (.pkl)")
model_file = st.file_uploader("Upload a new `.pkl` model file", type="pkl")

if model_file:
    try:
        with open("xgboost_views_model.pkl", "wb") as f:
            f.write(model_file.getbuffer())
        st.success("✅ Model file replaced successfully.")
    except Exception as e:
        st.error(f"❌ Failed to save model: {e}")

st.divider()

# --- Maintenance Utilities ---
st.subheader("🧹 Maintenance")

if st.button("🧽 Clear Cached Data"):
    try:
        shutil.rmtree("__pycache__", ignore_errors=True)
        st.cache_data.clear()  # OR st.cache_resource.clear() if using caching for model/data
        st.success("✅ Streamlit cache cleared.")
    except Exception as e:
        st.error(f"⚠️ Failed to clear cache: {e}")

st.divider()

# --- Show Current Model Info ---
st.subheader("🔎 Current Model Info")
try:
    model = joblib.load("xgboost_views_model.pkl")
    st.write(model)
except Exception as e:
    st.warning("No model loaded or error reading model.")
    st.error(e)
