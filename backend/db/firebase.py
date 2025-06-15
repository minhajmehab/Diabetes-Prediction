import os
import logging
from datetime import datetime
from typing import Dict, Any, Union

from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# ------------------ Logging Setup ------------------
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ------------------ Load Environment Variables ------------------
load_dotenv()

# ------------------ Firebase Initialization ------------------
FIREBASE_CRED = (
    "firebase_cred.json"
)
cred = credentials.Certificate(FIREBASE_CRED)
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()


def upload_patient_data_to_firebase(username: str, data: Dict[str, Any]) -> None:
    """
    Upload a patient's prediction record to Firestore.

    Args:
        username (str): The user identifier.
        data (dict): Patient prediction data.
    """
    try:
        record = {
            "username": username,
            "pregnancies": data.get("Pregnancies"),
            "glucose": data.get("Glucose"),
            "blood_pressure": data.get("BloodPressure"),
            "skin_thickness": data.get("SkinThickness"),
            "insulin": data.get("Insulin"),
            "bmi": data.get("BMI"),
            "diabetes_pedigree_function": data.get("DiabetesPedigreeFunction"),
            "age": data.get("Age"),
            "prediction_class": data.get("prediction"),
            "top_factors": data.get("top_factors"),
            "score": data.get("score"),
            "date": data.get("Date"),
        }
        doc_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        db_firestore.collection("users").document(username).collection("predictions").document(doc_id).set(record)
        logger.info(f"Patient data uploaded for user: {username}, document ID: {doc_id}")
    except Exception as e:
        logger.error(f"Error saving patient data to Firebase: {e}", exc_info=True)


def get_patient_data(username: str) -> Union[Dict[str, list], Dict[str, str]]:
    """
    Retrieve all prediction records for a given user.

    Args:
        username (str): The user identifier.

    Returns:
        dict: A dictionary with prediction data or error message.
    """
    try:
        docs = db_firestore.collection("users").document(username).collection("predictions").stream()
        results = [doc.to_dict() for doc in docs]
        logger.info(f"Retrieved {len(results)} prediction(s) for user: {username}")
        return {"predictions": results}
    except Exception as e:
        logger.error(f"Error retrieving patient data from Firebase: {e}", exc_info=True)
        return {"error": str(e)}
