# pages/2visualisations.py

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from prophet import Prophet
from prophet.plot import plot_plotly
from utils.data_utils import load_all_data

# Title and Introduction
st.title("📈 Data Visualizations")

# --- Upload New Data CSV ---
st.sidebar.subheader("📂 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload Video and Daily Views Data CSV", type="csv")

# --- Load Data ---
with st.spinner("Loading data..."):
    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file)
        st.success("Data uploaded successfully.")
        # Assuming the uploaded file contains both video data and daily views data, we split the data accordingly
        video_data = new_data[['Video title', 'Views', 'Video publish date', 'RPM (USD)', 'Likes per View', 
                               'Dislikes per View', 'Comments per View', 'Shares per View', 'Impressions',
                               'Impressionss click-through rate (%)', 'Subscribers', 'Subscribers gained', 
                               'Subscribers lost', 'Watch time', 'Publish Month', 'Publish Day', 'Publish Weekday', 
                               'Is Weekend', 'Average view Duration (sec)', 'Average Percentage viewed(%)', 
                               'Your Estmated Revenue (USD)', 'Performance']].copy()
        
        daily_views = new_data[['Video publish date', 'Views']].copy()  # Assuming these are the columns for daily views

    else:
        # Load the existing data if no new file is uploaded
        try:
            video_data, _, daily_views, _ = load_all_data()
        except Exception as e:
            st.error(f"❌ Failed to load data: {e}")
            st.stop()

# --- Handle Empty Data ---
if video_data.empty or daily_views.empty:
    st.warning("🚫 No video or daily view data available. Please upload the data and try again.")
    st.stop()

# --- Apply Date Filter ---
# st.sidebar.header("📅 Date Filter")
if "Video publish date" in daily_views.columns:
    daily_views["Video publish date"] = pd.to_datetime(daily_views["Video publish date"])
    min_date = daily_views["Video publish date"].min()
    max_date = daily_views["Video publish date"].max()

    date_range = st.sidebar.date_input("Select date range:", [min_date, max_date])

    if len(date_range) == 2:
        daily_views = daily_views[
            (daily_views["Video publish date"] >= pd.to_datetime(date_range[0])) & 
            (daily_views["Video publish date"] <= pd.to_datetime(date_range[1]))
        ].copy()

# --- Top Performing Videos ---
st.subheader("🔥 Top Performing Videos")

if "Views" in video_data.columns:
    top_videos = video_data.sort_values(by="Views", ascending=False).head(10)

    # Calculate lower and upper ranges for views (±10%)
    top_videos["view_lower"] = (top_videos["Views"] * 0.90).astype(int)  # Lower range (10% less)
    top_videos["view_upper"] = (top_videos["Views"] * 1.10).astype(int)  # Upper range (10% more)

    st.dataframe(top_videos[["Video title", "Views", "view_lower", "view_upper"]])

    # Bar chart for Top Performing Videos
    fig = px.bar(
        top_videos,
        x="Views",
        y="Video title",
        orientation="h",
        title="Top 10 Videos by Views",
        color="Views",  # Using color to visually differentiate based on Views
        color_continuous_scale="Viridis",  # Color scale applied to Views
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ 'Views' column is missing from video data.")

# --- Performance by Publish Month (Bar Chart) ---
st.subheader("📅 Performance by Publish Month")

if "Publish Month" in video_data.columns:
    performance_by_month = video_data.groupby("Publish Month")[["Views", "Subscribers gained", "Your Estmated Revenue (USD)"]].sum().reset_index()

    fig = px.bar(
        performance_by_month,
        x="Publish Month",
        y=["Views", "Subscribers gained", "Your Estmated Revenue (USD)"],
        title="Performance by Publish Month",
        barmode="stack",  # Stacked bar chart to show different metrics for each month
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ 'Publish Month' column is missing.")

# --- Revenue vs. Views (Scatter Plot) ---
st.subheader("💰 Views vs Revenue")

if "Views" in video_data.columns and "RPM (USD)" in video_data.columns and "Your Estmated Revenue (USD)" in video_data.columns:
    revenue_vs_views = video_data[["Views", "RPM (USD)", "Your Estmated Revenue (USD)"]]

    fig = px.scatter(
        revenue_vs_views,
        x="Views",
        y="Your Estmated Revenue (USD)",
        title="Views vs Revenue",
        color="RPM (USD)",
        color_continuous_scale="YlOrRd",  # Color scale for RPM
        labels={"Views": "Views", "Your Estmated Revenue (USD)": "Estimated Revenue (USD)", "RPM (USD)": "RPM (USD)"}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ 'Views', 'RPM (USD)', or 'Your Estmated Revenue (USD)' column is missing.")



# --- Click-Through Rate (CTR) vs. Impressions (Scatter Plot) ---
st.subheader("📊 Click-Through Rate (CTR) vs. Impressions")

if "Impressions" in video_data.columns and "Impressionss click-through rate (%)" in video_data.columns:
    ctr_vs_impressions = video_data[["Video title", "Impressions", "Impressionss click-through rate (%)"]]

    fig = px.scatter(
        ctr_vs_impressions,
        x="Impressions",
        y="Impressionss click-through rate (%)",
        title="CTR vs. Impressions",
        hover_name="Video title",
        color="Impressionss click-through rate (%)",
        color_continuous_scale="Viridis",
        labels={"Impressions": "Impressions", "Impressionss click-through rate (%)": "CTR (%)"}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ 'Impressions' or 'Impressionss click-through rate (%)' columns are missing.")
