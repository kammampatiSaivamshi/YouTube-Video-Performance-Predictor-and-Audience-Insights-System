import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Title and Introduction
st.title("💬 Sentiment Analysis")

# --- Upload Comments Data CSV ---
st.sidebar.subheader("📂 Upload Comments Data")
uploaded_file = st.sidebar.file_uploader("Upload Comments Data CSV", type="csv")

# --- Load Data ---
if uploaded_file is not None:
    try:
        comments_data = pd.read_csv(uploaded_file)
        st.success("Comments data uploaded successfully.")
    except Exception as e:
        st.error(f"❌ Failed to load the uploaded file: {e}")
        st.stop()

else:
    st.warning("Please upload a comments dataset to proceed.")
    st.stop()

# --- Check for Missing or Invalid Columns ---
required_cols = {"Sentiment", "Comments", "DateOnly", "Like_Count", "Reply_Count", "user_ID", "VidId"}
if not all(col in comments_data.columns for col in required_cols):
    st.error("❌ Required columns ('Sentiment', 'Comments', 'DateOnly', 'Like_Count', 'Reply_Count', 'user_ID', 'VidId') are missing from the comments dataset.")
    st.stop()

# --- Create Cleaned Comments Column ---
comments_data['clean_comment'] = comments_data['Comments'].str.replace(r'[^\w\s]', '', regex=True)  # Remove punctuation
comments_data['clean_comment'] = comments_data['clean_comment'].str.replace(r'\s+', ' ', regex=True).str.strip()  # Remove extra spaces

# --- Filter Comments by Sentiment ---
st.subheader("🔍 View Comments by Sentiment")

try:
    # Clean the Sentiment column by stripping spaces and converting to lowercase
    comments_data['Sentiment'] = comments_data['Sentiment'].str.strip().str.lower()

    sentiment_option = st.selectbox("Choose Sentiment Type", ["positive", "neutral", "negative"])

    # Filter comments based on sentiment choice
    filtered_comments = comments_data[comments_data['Sentiment'] == sentiment_option]

    st.write(f"Showing {len(filtered_comments)} **{sentiment_option}** comments:")

    # Allow users to search comments for keywords
    search_query = st.text_input("Search comments for a keyword")
    if search_query:
        filtered_comments = filtered_comments[filtered_comments['Comments'].str.contains(search_query, case=False, na=False)]
        st.write(f"Showing {len(filtered_comments)} comments containing '{search_query}':")
    
    # Display the filtered comments
    if len(filtered_comments) > 0:
        st.dataframe(filtered_comments[['Comment_ID', 'Comments', 'Sentiment']].head(20))
    else:
        st.warning("No comments found matching the filter.")

except Exception as e:
    st.warning(f"⚠️ Error displaying filtered comments: {e}")

    
# --- Sentiment Breakdown (Pie Chart or Bar Chart) ---
st.subheader("📊 Sentiment Breakdown")

try:
    sentiment_counts = comments_data['Sentiment'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    
    fig = px.pie(sentiment_counts, values='Count', names='Sentiment', title="Sentiment Breakdown", hole=0.4)
    st.plotly_chart(fig)
except Exception as e:
    st.warning(f"⚠️ Could not display sentiment breakdown: {e}")


# --- Sentiment Analysis Over Time (Line Chart) ---
st.subheader("📅 Sentiment Analysis Over Time")

try:
    sentiment_over_time = comments_data.groupby(['DateOnly', 'Sentiment']).size().reset_index(name='Count')

    fig = px.line(sentiment_over_time, x="DateOnly", y="Count", color="Sentiment", 
                  title="Sentiment Analysis Over Time", markers=True)
    st.plotly_chart(fig)
except Exception as e:
    st.warning(f"⚠️ Could not display sentiment analysis over time: {e}")

# --- Total Likes per Comment (Bar Chart or Histogram) ---
st.subheader("👍 Total Likes per Comment")

try:
    fig = px.histogram(comments_data, x="Like_Count", title="Total Likes per Comment", nbins=30)
    st.plotly_chart(fig)
except Exception as e:
    st.warning(f"⚠️ Could not display likes per comment: {e}")

# --- Reply Count Distribution (Histogram or Bar Chart) ---
st.subheader("💬 Reply Count Distribution")

try:
    fig = px.histogram(comments_data, x="Reply_Count", title="Reply Count Distribution", nbins=30)
    st.plotly_chart(fig)
except Exception as e:
    st.warning(f"⚠️ Could not display reply count distribution: {e}")

# --- Top Comments by Like Count (Bar Chart) ---
st.subheader("🏆 Top Comments by Like Count")

try:
    top_comments = comments_data[['Comments', 'Like_Count']].sort_values(by="Like_Count", ascending=False).head(10)
    fig = px.bar(top_comments, x='Comments', y='Like_Count', title="Top Comments by Like Count", color='Like_Count', 
                 color_continuous_scale="Viridis", labels={'Like_Count': 'Likes'})
    st.plotly_chart(fig)
except Exception as e:
    st.warning(f"⚠️ Could not display top comments by like count: {e}")

# --- Comment Frequency Over Time (Line Chart) ---
st.subheader("📅 Comment Frequency Over Time")

try:
    comment_frequency = comments_data.groupby(['DateOnly']).size().reset_index(name='Comment Count')

    fig = px.line(comment_frequency, x="DateOnly", y="Comment Count", title="Comment Frequency Over Time", markers=True)
    st.plotly_chart(fig)
except Exception as e:
    st.warning(f"⚠️ Could not display comment frequency over time: {e}")



# --- User Engagement by User (Bar Chart or Scatter Plot) ---
st.subheader("👥 User Engagement by User")

try:
    user_engagement = comments_data.groupby('user_ID')[['Like_Count', 'Reply_Count']].sum().reset_index()

    fig = px.scatter(user_engagement, x="Like_Count", y="Reply_Count", color="user_ID", 
                     title="User Engagement by User", labels={'Like_Count': 'Likes', 'Reply_Count': 'Replies'})
    st.plotly_chart(fig)
except Exception as e:
    st.warning(f"⚠️ Could not display user engagement by user: {e}")

# --- Comment Frequency per Video (Bar Chart) ---
st.subheader("🎥 Comment Frequency per Video")

try:
    comment_frequency_per_video = comments_data.groupby('VidId').size().reset_index(name='Comment Count')

    fig = px.bar(comment_frequency_per_video, x="VidId", y="Comment Count", title="Comment Frequency per Video", color="Comment Count",
                 color_continuous_scale="Viridis")
    st.plotly_chart(fig)
except Exception as e:
    st.warning(f"⚠️ Could not display comment frequency per video: {e}")
