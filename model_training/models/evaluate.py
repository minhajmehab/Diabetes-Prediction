import logging
from typing import Dict
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logger = logging.getLogger(__name__)

def evaluate_model(
    model: BaseEstimator,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Dict[str, float]:
    """
    Evaluate a trained model on test data.

    Parameters
    ----------
    model : BaseEstimator
        The trained scikit-learn model.
    X_test : pd.DataFrame
        Test features.
    y_test : pd.Series
        True test labels.

    Returns
    -------
    Dict[str, float]
        Dictionary with accuracy, precision, recall, and f1 score.
    """
    logger.info("Evaluating model.")
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0)
    }
    logger.info(f"Evaluation metrics: {metrics}")
    return metrics
