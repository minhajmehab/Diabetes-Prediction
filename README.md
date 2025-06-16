# Diabetes Prediction Web Application

A full-stack web application for predicting diabetes using machine learning models. The project allows users to upload medical reports, extract patient data, make predictions using trained models, and view their prediction history.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Model Training](#model-training)

---

## Features

- User authentication (Firebase)
- Upload and extract data from medical reports (PDF)
- Diabetes prediction using classical ML
- Model explainability with SHAP visualizations for feature importance
- View prediction history
- Responsive frontend dashboard

---

## Project Structure

```
.env
.gitignore
docker-compose.yml
firebase_cred.json
README.md
requirements.txt
backend/
    Dockerfile
    main.py
    api/
    auth/
    db/
    models/
    services/
frontend/
    dashboard.html
    Dockerfile
    history.html
    index.html
    assets/
        css/
        js/
model_training/
    run_train_pipeline.py
    data/
    dataset/
    features/
    models/
saved_models/
    model.joblib
```

---

## Getting Started

### Prerequisites

- Python 3.12
- Docker (recommended)

### Installation

1. **Clone the repository**
    ```sh
    git clone https://github.com/yourusername/diabetes-prediction.git
    cd diabetes-prediction
    ```

2. **Set up Firebase credentials**
    - Obtain your Firebase service account JSON file from the Firebase Console.
    - Save it as `firebase_cred.json` in the project root

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

#### Using Docker (Recommended)

```sh
docker-compose up --build
```

#### Manual Run

- **Backend:**
    ```sh
    cd backend
    uvicorn main:app --reload
    ```
- **Frontend:**
    Serve the `frontend/` directory using any static server, e.g.:
    ```sh
    cd frontend
    python -m http.server 8080
    ```

---

## Usage

1. Open the frontend in your browser (`index.html` or via the running server).
2. Register or log in.
3. Upload a medical report (PDF).
4. Review extracted data and make a prediction.
5. View prediction results and history.

---

## API Endpoints

| Endpoint                        | Method | Description                              |
|----------------------------------|--------|------------------------------------------|
| `/auth/login`                   | POST   | User login                               |
| `/auth/register`                | POST   | User registration                        |
| `/api/extract-data`             | POST   | Extract patient data from uploaded PDF    |
| `/classical/predict`            | POST   | Predict using classical ML model          |
| `/classical/get-patient-data`   | GET    | Get user's prediction history             |

---

## Model Training

To retrain or update the models:

```sh
cd model_training
python run_train_pipeline.py
```
Trained models are saved in the `saved_models/` directory.

---

## Why Random Forest Was Chosen for Diabetes Type Prediction

- **Handles Complex Relationships:**  
  Diabetes datasets often contain non-linear interactions between features (e.g., glucose levels, BMI, insulin resistance). Random Forest excels at capturing these intricate patterns without assuming linearity, making it ideal for medical data where multiple factors interact unpredictably.

- **Robustness to Noise and Outliers:**  
  Medical data (like Kaggle's diabetes datasets) frequently include measurement errors or outliers. Random Forest’s ensemble approach (averaging predictions from many decision trees) reduces overfitting and minimizes the impact of noisy data, ensuring more reliable predictions.

- **Automatic Feature Importance:**  
  The model provides intrinsic feature importance scores, revealing which factors (e.g., glucose levels, age, BMI) most influence diabetes type prediction. This aids in interpreting results clinically—critical for healthcare applications.

- **Handles High-Dimensional Data Efficiently:**  
  Even with numerous features (e.g., pregnancies, blood pressure, skin thickness), Random Forest maintains accuracy by selecting random subsets of features for each tree, preventing dominance by irrelevant variables.

- **Requires Minimal Preprocessing:**  
  Unlike models sensitive to feature scaling (e.g., SVM, logistic regression), Random Forest works well with raw or unscaled data, reducing preprocessing steps and potential information loss.

---
