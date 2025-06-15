import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import NoReturn
from model_training.data.load_data import load_data
from model_training.features.preprocess import preprocess_data
from model_training.models.model_trainer import train_model
from model_training.models.evaluate import evaluate_model
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

def main() -> NoReturn:
    """
    Main function to run the training and evaluation pipeline.
    """
    dataset_csv_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'dataset',
        'Healthcare-Diabetes.csv'
    )
    print(f"Current directory: {dataset_csv_path}")

    try:
        # Load
        df = load_data(local_path=dataset_csv_path)
        logger.info("Data loaded successfully.")

        # Preprocess
        X_train, X_test, y_train, y_test = preprocess_data(df)
        logger.info("Data preprocessed successfully.")

        model = RandomForestClassifier(n_estimators=100)

        model = train_model(model, X_train, y_train)
        logger.info("Model trained successfully.")

        # Evaluate
        metrics = evaluate_model(model, X_test, y_test)
        logger.info(f"Evaluation metrics: {metrics}")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()
