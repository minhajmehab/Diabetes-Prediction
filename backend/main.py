import os
import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ------------------ Logging Setup ------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# ------------------ Ensure `src` is Importable ------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.routes import router
from services.utils import load_model

# ------------------ App Setup ------------------
app = FastAPI(title="Diabetes Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Load ML Model ------------------
# MODEL_PATH = os.path.abspath(
#     os.path.join(os.path.dirname(__file__), '..', 'saved_models', 'model.joblib')
# )

MODEL_PATH = "saved_models/model.joblib"


try:
    model = load_model(MODEL_PATH)
    app.state.model = model
    logger.info("Model successfully loaded and stored in app state.")
except Exception as e:
    logger.error(f"Failed to load model at startup: {e}", exc_info=True)

# ------------------ Register Routes ------------------
app.include_router(router)

# ------------------ Entry Point ------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
