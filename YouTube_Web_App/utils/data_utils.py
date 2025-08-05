import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_all_data(data_dir="data", verbose=True):
    """
    Load all required CSV datasets from the specified data/ directory.

    Args:
        data_dir: Directory where CSV files are stored.
        verbose: Flag for logging information.

    Returns:
        Tuple of DataFrames: (video_data, geo_data, daily_views, comments)
    """
    # Dictionary to map DataFrame names to file paths
    files = {
        "video_data": "Processed_Video_Data.csv",
        "geo_data": "Aggregated_Metrics_By_Country_And_Subscriber_Status.csv",
        "daily_views": "Daily_Views_Over_Time.csv",
        "comments": "Processed_Comments_Sentiment.csv"
    }

    dataframes = {}

    # Check for each file and load if it exists
    for key, file_name in files.items():
        path = os.path.join(data_dir, file_name)
        
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                dataframes[key] = df
                if verbose:
                    st.info(f"📁 Loaded: {file_name} ({len(df)} rows)")
            except Exception as e:
                st.error(f"❌ Failed to load {file_name}: {e}")
                dataframes[key] = pd.DataFrame()
        else:
            if verbose:
                st.warning(f"⚠️ {file_name} not found in {data_dir}/")
            dataframes[key] = pd.DataFrame()

    # Return dataframes, ensuring each key is present
    return (
        dataframes.get("video_data", pd.DataFrame()),
        dataframes.get("geo_data", pd.DataFrame()),
        dataframes.get("daily_views", pd.DataFrame()),
        dataframes.get("comments", pd.DataFrame())
    )

def check_and_upload_files(data_dir="data"):
    """
    Helper function to allow users to upload CSV files if any data is missing.

    Args:
        data_dir: Directory where files should be uploaded.
    """
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        st.info(f"Created directory: {data_dir}")

    uploaded_files = st.file_uploader("Upload missing files", accept_multiple_files=True, type=["csv"])
    
    missing_files = []
    required_files = {
        "Processed_Video_Data.csv": "video_data",
        "Aggregated_Metrics_By_Country_And_Subscriber_Status.csv": "geo_data",
        "Daily_Views_Over_Time.csv": "daily_views",
        "Processed_Comments_Sentiment.csv": "comments"
    }
    
    for file_name, data_key in required_files.items():
        if not os.path.exists(os.path.join(data_dir, file_name)):
            missing_files.append(file_name)

    if missing_files:
        st.warning(f"⚠️ Missing the following required files: {', '.join(missing_files)}")
    else:
        st.success("All required files are present!")
        
    for uploaded_file in uploaded_files:
        with open(os.path.join(data_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ Uploaded: {uploaded_file.name}")
    
    # Return updated status
    return missing_files
