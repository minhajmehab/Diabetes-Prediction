import logging
from datetime import timedelta
from typing import Dict

from fastapi import (
    APIRouter, HTTPException, Depends, status, Request, File, UploadFile
)
from fastapi.security import OAuth2PasswordRequestForm
import pandas as pd

from db.firebase import upload_patient_data_to_firebase, get_patient_data
from models.schemas import (
    Token, PatientData, PredictionResponse, MessageResponse,
    PdfExtractionResponse, FirebaseResponse
)
from auth.auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
from services.users import authenticate_user
from services.utils import prepare_features, extract_medical_data_from_pdf, predict

# Set up logger
logger = logging.getLogger(__name__)

router = APIRouter()
user_extracted_data: Dict[str, dict] = {}


@router.get("/", response_model=MessageResponse)
def root():
    """Root endpoint"""
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the Diabetes Prediction API!"}


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint to get access token"""
    logger.info(f"Login attempt for user: {form_data.username}")
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    logger.info(f"Access token created for user: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/classical/extract-patient-data", response_model=PdfExtractionResponse)
async def extract_from_pdf(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    request: Request = None
):
    """
    Extracts medical data from uploaded PDF and stores it for the current user.
    """
    logger.info(f"Extracting data from PDF for user: {current_user['username']}")
    try:
        contents = await file.read()
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(contents)

        pdf_extracted_data = extract_medical_data_from_pdf(temp_path)
        if not pdf_extracted_data:
            logger.warning("Could not extract data from PDF.")
            raise HTTPException(status_code=400, detail="Could not extract data from PDF.")

        user_extracted_data[current_user["username"]] = pdf_extracted_data
        logger.info(f"Extracted data stored for user: {current_user['username']}")
        return {"extracted_data": pdf_extracted_data}
    except Exception as e:
        logger.error(f"Error extracting data from PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/classical/predict", response_model=PredictionResponse)
async def predict_diabetes(
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    logger.info(f"Prediction requested by user: {current_user['username']}")
    try:
        patient_data = user_extracted_data.get(current_user["username"])
        date = None
        if patient_data and "Date" in patient_data:
            date = {'Date': patient_data.pop('Date', None)}

        if not patient_data:
            logger.warning("No extracted data found for user.")
            raise HTTPException(
                status_code=400,
                detail="No extracted data found for user. Please upload a PDF first."
            )

        input_patient_data = PatientData(**patient_data)
        model = request.app.state.model
        df = pd.DataFrame([input_patient_data.dict()])
        X = prepare_features(df)
        prediction_class, top_factors, score = predict(model, X)

        response_data = {
            "prediction": prediction_class,
            "top_factors": top_factors,
            "score": score
        }

        user_extracted_data[current_user["username"]].update(response_data)
        if date:
            user_extracted_data[current_user["username"]].update(date)

        upload_patient_data_to_firebase(
            current_user["username"],
            user_extracted_data[current_user["username"]]
        )
        logger.info(f"Prediction completed and data uploaded for user: {current_user['username']}")
        return response_data

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/classical/get-patient-data", response_model=FirebaseResponse)
def get_patient_data_endpoint(
    current_user: dict = Depends(get_current_user)
):
    """
    Returns the patient data for the current user from Firebase.
    """
    logger.info(f"Fetching patient data for user: {current_user['username']}")
    try:
        records = get_patient_data(current_user["username"])
        if "error" in records:
            logger.error(f"Error from Firebase: {records['error']}")
            raise HTTPException(status_code=500, detail=records["error"])

        return {"extracted_data": records["predictions"]}
    except Exception as e:
        logger.error(f"Error fetching patient data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transformer/predict", response_model=MessageResponse)
def transformer():
    """Transformer endpoint (not implemented)"""
    logger.info("Transformer endpoint accessed.")
    return {"message": "NOT IMPLEMENTED YET. Please use the classical model for predictions."}


@router.get("/neural/predict", response_model=MessageResponse)
def neural_network():
    """Neural network endpoint (not implemented)"""
    logger.info("Neural network endpoint accessed.")
    return {"message": "NOT IMPLEMENTED YET. Please use the classical model for predictions."}
