from typing import Dict, List, Any
from pydantic import BaseModel


class Token(BaseModel):
    """JWT Token schema"""
    access_token: str
    token_type: str


class PatientData(BaseModel):
    """Input features for diabetes prediction"""
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int


class PredictionResponse(BaseModel):
    """Prediction output from the model"""
    prediction: int
    top_factors: Dict[str, float]
    score: float


class MessageResponse(BaseModel):
    """Generic response for status messages"""
    message: str


class PdfExtractionResponse(BaseModel):
    """Response after extracting data from PDF"""
    extracted_data: dict


class FirebaseResponse(BaseModel):
    """Firebase prediction history response"""
    extracted_data: List[Dict[str, Any]]
