# pages/1predictions.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import io

from utils.model_utils import load_model, predict_views
from utils.data_utils import load_all_data
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# Page Configurations
st.set_page_config(page_title="Predict Video Performance", layout="wide")
st.markdown("## 📊 Predict Video Performance")
st.markdown("Use historical video data to predict future views using a trained XGBoost model.")
st.markdown("---")

# Load Model and Data
model = load_model()
if model is None:
    st.error("❌ Model failed to load. Please ensure the model file is available and try again.")
    st.stop()

video_data, _, _, _ = load_all_data()
expected_columns = list(video_data.drop(columns=["video_id", "title", "views"], errors="ignore").columns)

# --- Input Tabs ---
tab1, tab2 = st.tabs(["🎯 Use Sample Row", "📄 Upload New Data"])
input_data = None

with tab1:
    idx = st.selectbox("Select a video row:", video_data.index)
    input_data = video_data.drop(columns=["video_id", "title", "views"], errors="ignore").loc[[idx]]
    st.write("Selected Video Data:")
    st.dataframe(video_data.loc[[idx]])

with tab2:
    uploaded = st.file_uploader("Upload CSV with same feature columns as training data", type="csv")
    if uploaded:
        uploaded_df = pd.read_csv(uploaded)
        uploaded_cols = uploaded_df.columns.str.strip().str.lower()
        missing_cols = set(map(str.lower, expected_columns)) - set(uploaded_cols)

        if missing_cols:
            st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
        else:
            st.success("✅ Uploaded data has the expected schema.")
            st.write("Uploaded Data Preview:")
            st.dataframe(uploaded_df)

            if st.checkbox("🔁 Predict All Rows"):
                clean_input = uploaded_df[expected_columns]
                try:
                    preds = predict_views(model, clean_input)
                    results_df = uploaded_df.copy()
                    results_df["Predicted_Views"] = preds.astype(int)
                    st.dataframe(results_df[["title", "Predicted_Views"]] if "title" in results_df else results_df)

                    csv = results_df.to_csv(index=False).encode("utf-8")
                    st.download_button("📅 Download Predictions", data=csv, file_name="predictions.csv", mime="text/csv")
                except Exception as e:
                    st.error(f"❌ Prediction failed: {e}")
            else:
                row_idx = st.selectbox("Select a row from uploaded data:", uploaded_df.index)
                input_data = uploaded_df.drop(columns=["video_id", "title", "views"], errors="ignore").loc[[row_idx]]
                st.write("Selected Row Data:")
                st.dataframe(uploaded_df.loc[[row_idx]])

# --- Predict and Display ---
if input_data is not None and not input_data.empty:
    try:
        prediction = predict_views(model, input_data)
        error_margin = prediction * 0.10  # ±10% for confidence range
        lower = int(prediction - error_margin)
        upper = int(prediction + error_margin)

        st.markdown("### 📈 Predicted Views")
        st.metric(label="Estimated Views", value=f"{int(prediction):,}")
        st.markdown(f"📉 **Estimated Range:** {lower:,} to {upper:,} views (±10%)")
    except Exception as e:
        st.error(f"❌ Prediction error: {e}")

# --- Feature Importance ---
st.markdown("---")
st.subheader("🔍 Feature Importance")

if hasattr(model, 'feature_importances_'):
    feature_names = model.get_booster().feature_names
    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    # Optional tooltip descriptions
    feature_explanations = {
        "avg_watch_time": "Average watch time per view in seconds",
        "likes_ratio": "Ratio of likes to total reactions",
        "comment_sentiment": "Average sentiment score from comments"
        # Add more as needed
    }
    importance_df["Explanation"] = importance_df["Feature"].map(feature_explanations)

    fig = px.bar(
        importance_df.head(15),
        x="Importance",
        y="Feature",
        orientation="h",
        color="Importance",
        color_continuous_scale="Turbo",
        title="Top Feature Importances",
        hover_data=["Explanation"]
    )
    fig.update_layout(
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        font=dict(size=13),
        title_font=dict(size=20),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Downloadable Report ---
    st.download_button(
        label="📄 Download Feature Importance Report (CSV)",
        data=importance_df.to_csv(index=False),
        file_name="feature_importance_report.csv",
        mime="text/csv"
    )
