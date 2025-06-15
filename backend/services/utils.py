import logging
import re
from typing import Any, Dict, Optional, Tuple

import joblib
import matplotlib.pyplot as plt  # Unused, remove if not needed
import numpy as np
import pandas as pd
import pdfplumber

# ------------------ Logging Setup ------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def load_model(model_path: str) -> Any:
    """
    Load a trained model from disk using joblib.

    Args:
        model_path (str): Path to the saved model file.

    Returns:
        Any: The loaded model object.
    """
    logger.info(f"Loading model from {model_path}")
    model = joblib.load(model_path)
    logger.info("Model loaded successfully.")
    return model


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare features by removing unwanted columns.

    Args:
        df (pd.DataFrame): Input DataFrame with features.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    drop_cols = [col for col in ['Outcome', 'Id'] if col in df.columns]
    return df.drop(columns=drop_cols)


def extract_medical_data_from_pdf(pdf_path: str) -> Optional[Dict[str, Any]]:
    """
    Extract relevant medical data fields from a PDF document.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        dict or None: Dictionary of extracted fields, or None if extraction fails.
    """
    data = {
        'Pregnancies': None,
        'Glucose': None,
        'BloodPressure': None,
        'SkinThickness': None,
        'Insulin': None,
        'BMI': None,
        'DiabetesPedigreeFunction': None,
        'Age': None,
        'Date': None
    }

    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        patterns = {
            'Pregnancies': r'Pregnancies\s+(\d+)',
            'Glucose': r'Glucose\s*\(.*?\)\s*(\d+(?:\.\d+)?)',
            'BloodPressure': r'Blood Pressure\s*\(.*?\)\s*(\d+(?:\.\d+)?)',
            'SkinThickness': r'Skin Thickness\s*\(.*?\)\s*(\d+(?:\.\d+)?)',
            'Insulin': r'Insulin\s*\(.*?\)\s*(\d+(?:\.\d+)?)',
            'BMI': r'BMI\s*\(.*?\)\s*(\d+(?:\.\d+)?)',
            'DiabetesPedigreeFunction': r'Diabetes Pedigree Function\s+(\d+(?:\.\d+)?)',
            'Age': r'Age\s*\(.*?\)\s*(\d+(?:\.\d+)?)',
            'Date': r'\b(\d{2}-\d{2}-\d{4})\b'
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1)
                if key in ['Pregnancies', 'Age']:
                    data[key] = int(value)
                elif key == 'Date':
                    data[key] = value
                else:
                    data[key] = float(value)

        return data

    except Exception as e:
        logger.error(f"Error reading PDF: {e}", exc_info=True)
        return None


def predict(model: Any, X: pd.DataFrame) -> Tuple[pd.Series, Dict[str, float], float]:
    """
    Make prediction and extract top influential features (if positive).

    Args:
        model (Any): Trained model.
        X (pd.DataFrame): Feature DataFrame with a single sample.

    Returns:
        Tuple containing:
            - pd.Series: Prediction result.
            - dict: Top influencing features for positive prediction.
            - float: Confidence score (probability for class 1).
    """
    logger.info("Making predictions.")
    preds = model.predict(X)
    pred_int = int(preds[0])

    pred_score = model.predict_proba(X)[0][pred_int]


    top_factors = {}
    prediction_percent = 0.0

    try:
        proba = model.predict_proba(X)[0][1]  # Probability of class 1
        prediction_percent = round(proba * 100, 2)

        if pred_int == 1:
            feature_importance = model.feature_importances_
            top_features_idx = np.argsort(feature_importance)[-3:][::-1]
            top_features = X.columns[top_features_idx].tolist()
            top_values = X.iloc[0, top_features_idx].tolist()
            top_factors = {feat: val for feat, val in zip(top_features, top_values)}

    except Exception as e:
        logger.error(f"Feature importance extraction failed: {e}", exc_info=True)

    # return pd.Series(preds, name="Prediction"), top_factors, prediction_percent
    return pred_int, top_factors, pred_score