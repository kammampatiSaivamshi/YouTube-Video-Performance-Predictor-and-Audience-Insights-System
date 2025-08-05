import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_utils import load_all_data

st.title("🌍 Geographic Insights for New YouTubers")

# --- File Uploader for External Data ---
st.sidebar.subheader("📂 Upload External Data")
uploaded_file = st.sidebar.file_uploader("Upload Video Data CSV", type="csv")

# --- Load Data ---
if uploaded_file is not None:
    try:
        geo_data = pd.read_csv(uploaded_file)
        st.success("External data uploaded successfully.")
    except Exception as e:
        st.error(f"❌ Failed to load the uploaded file: {e}")
        st.stop()

else:
    # If no file is uploaded, load the existing data
    try:
        _, geo_data, _, _ = load_all_data()
    except Exception as e:
        st.error(f"❌ Failed to load default video data: {e}")
        st.stop()

# --- Check for Empty Data ---
if geo_data.empty:
    st.warning("No data available.")
    st.stop()

# --- Check for Missing Columns ---
required_columns = ['Country Code', 'Is Subscribed', 'Views', 'Video Length', 'Video Title', 'Video Likes Added', 
                    'Video Dislikes Added', 'Video Likes Removed', 'User Subscriptions Added', 'User Subscriptions Removed', 
                    'Average View Percentage', 'Average Watch Time']
missing_columns = [col for col in required_columns if col not in geo_data.columns]
if missing_columns:
    st.warning(f"⚠️ Missing columns: {', '.join(missing_columns)}")

# --- Country Selection Widget ---
st.sidebar.header("🌍 Select a Country")
countries = geo_data['Country Code'].unique()  # Get unique countries in the dataset

# Allow the user to select a single country
selected_country = st.sidebar.selectbox("Choose a country to visualize:", countries)

# --- Filter Data by Selected Country ---
filtered_data = geo_data[geo_data['Country Code'] == selected_country]

# --- Metric Selection ---
st.sidebar.header("🎯 Metric Selection")
numeric_cols = geo_data.select_dtypes(include='number').columns.tolist()

if not numeric_cols:
    st.error("⚠️ No numeric columns found in the dataset.")
    st.stop()

metric = st.sidebar.selectbox("Select a metric to visualize:", numeric_cols, index=0)

# --- Top Performing Videos by Views ---
st.subheader(f"📈 Top Performing Videos by Views (Country: {selected_country})")
try:
    top_videos = filtered_data.sort_values(by="Views", ascending=False).head(10)

    fig_top_videos = px.bar(
        top_videos,
        x="Video Title",
        y="Views",
        title="Top 10 Videos by Views",
        color="Views",
        color_continuous_scale="Blues",
        labels={"Views": "Number of Views"}
    )
    st.plotly_chart(fig_top_videos)
except Exception as e:
    st.warning(f"⚠️ Could not generate top videos chart: {e}")

# --- Likes and Dislikes Breakdown ---
st.subheader(f"👍 Likes and Dislikes Breakdown (Country: {selected_country})")
try:
    engagement_data = filtered_data[['Video Title', 'Video Likes Added', 'Video Dislikes Added']].sort_values(by="Video Likes Added", ascending=False).head(10)

    fig_engagement = px.bar(
        engagement_data,
        x="Video Title",
        y=["Video Likes Added", "Video Dislikes Added"],
        title="Likes and Dislikes Breakdown",
        labels={"Video Likes Added": "Likes", "Video Dislikes Added": "Dislikes"},
        color_discrete_sequence=["green", "red"]
    )
    st.plotly_chart(fig_engagement)
except Exception as e:
    st.warning(f"⚠️ Could not generate likes and dislikes chart: {e}")

# --- Subscriber Growth ---
st.subheader(f"📈 Subscriber Growth vs Views (Country: {selected_country})")
try:
    filtered_data["Subscriber Growth"] = filtered_data["User Subscriptions Added"] - filtered_data["User Subscriptions Removed"]

    fig_subscriber_growth = px.scatter(
        filtered_data,
        x="Views",
        y="Subscriber Growth",
        title="Subscriber Growth vs Video Views",
        labels={"Views": "Views", "Subscriber Growth": "Subscriber Growth"},
        size="Views",
        color="Video Length",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_subscriber_growth)
except Exception as e:
    st.warning(f"⚠️ Could not generate subscriber growth vs views chart: {e}")

# --- Average Watch Time vs Views ---
st.subheader(f"📈 Average Watch Time vs Views for {selected_country}")
try:
    fig_watch_time = px.scatter(
        filtered_data,
        x="Average Watch Time",
        y="Views",
        title="Average Watch Time vs Views",
        color="Video Length",
        labels={"Average Watch Time": "Average Watch Time (min)", "Views": "Views"},
        size="Views",
        color_continuous_scale="Plasma"
    )
    st.plotly_chart(fig_watch_time)
except Exception as e:
    st.warning(f"⚠️ Could not generate average watch time vs views chart: {e}")

# --- Views by Video Length ---
st.subheader(f"🎥 {metric} by Video Length (Country: {selected_country})")
try:
    views_by_length = filtered_data.groupby("Video Length")[metric].sum().reset_index()

    fig_views_by_length = px.bar(
        views_by_length,
        x="Video Length",
        y=metric,
        title=f"{metric} by Video Length",
        color=metric,
        color_continuous_scale="RdYlGn",
        labels={metric: f"{metric} (Units)"}
    )
    st.plotly_chart(fig_views_by_length)
except Exception as e:
    st.warning(f"⚠️ Could not generate {metric} by video length chart: {e}")
