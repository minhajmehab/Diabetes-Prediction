import logging
from typing import Any
import pandas as pd
from sklearn.base import BaseEstimator
import joblib
import os

logger = logging.getLogger(__name__)


def train_model(
    model: BaseEstimator,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_dir: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'saved_models')
    ),
    model_filename: str = "model.joblib"
) -> BaseEstimator:
    """
    Train a scikit-learn model and save it to disk.

    Parameters
    ----------
    model : BaseEstimator
        The scikit-learn model to train.
    X_train : pd.DataFrame
        Training features.
    y_train : pd.Series
        Training target.
    model_dir : str, optional
        Directory to save the trained model (default is 'artifacts').
    model_filename : str, optional
        Filename for the saved model (default is 'model.joblib').

    Returns
    -------
    BaseEstimator
        The trained model.
    """
    print("Saving model to:", model_dir)
    print("*******************************************************")

    logger.info(f"Training model: {model.__class__.__name__}")
    model.fit(X_train, y_train)
    logger.info("Model training complete.")

    # Ensure the model directory exists
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, model_filename)
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")

    return model


