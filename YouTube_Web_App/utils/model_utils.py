import joblib
import os
import pandas as pd
import streamlit as st

@st.cache_resource
def load_model(model_path="xgboost_views_model.pkl", verbose=True):
    """
    Load the pre-trained model from the specified path.
    """
    if not os.path.exists(model_path):
        if verbose:
            st.error(f"❌ Model file not found at `{model_path}`")
        return None

    try:
        model = joblib.load(model_path)
        if verbose:
            st.success(f"✅ Model loaded from `{model_path}`")
        return model
    except Exception as e:
        if verbose:
            st.error(f"❌ Error loading model: {e}")
        return None

def predict_views(model, input_data):
    """
    Predict views using the trained model.
    
    Parameters:
    - model: The trained machine learning model (e.g., XGBoost)
    - input_data: Pandas DataFrame with features required by the model
    
    Returns:
    - Predicted view count
    """
    if model is None:
        raise ValueError("❌ Model not loaded. Please load a valid model first.")
    
    # Check input data type
    if not isinstance(input_data, pd.DataFrame):
        raise ValueError("❌ Input data must be a pandas DataFrame.")
    
    # Load expected features (from trained model)
    expected_features = model.get_booster().feature_names
    
    # Ensure all expected features exist in input
    missing = [col for col in expected_features if col not in input_data.columns]
    if missing:
        raise ValueError(f"❌ Missing features in input data: {missing}")

    # Drop extra columns and reorder to match model's expected features
    input_clean = input_data[expected_features]
    
    try:
        prediction = model.predict(input_clean)[0]
        return prediction
    except Exception as e:
        raise ValueError(f"❌ Error during prediction: {e}")
