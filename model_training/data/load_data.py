import logging
from typing import Optional
import pandas as pd

logger = logging.getLogger(__name__)

def load_data(
    url: Optional[str] = None,
    local_path: Optional[str] = None
) -> pd.DataFrame:
    """
    Load dataset from a URL or local CSV file.

    Parameters
    ----------
    url : str, optional
        URL to the CSV file.
    local_path : str, optional
        Local path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.

    Raises
    ------
    ValueError
        If neither url nor local_path is provided.
    FileNotFoundError
        If the local file does not exist.
    """
    column_names = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
        'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome'
    ]
    if url:
        logger.info(f"Loading data from URL: {url}")
        df = pd.read_csv(url, names=column_names)
    elif local_path:
        logger.info(f"Loading data from local path: {local_path}")
        try:
            df = pd.read_csv(local_path)
        except FileNotFoundError as e:
            logger.error(f"File not found: {local_path}")
            raise e
    else:
        logger.error("No data source provided. Provide either url or local_path.")
        raise ValueError("Provide either url or local_path")
    logger.info(f"Data loaded successfully with shape: {df.shape}")
    return df
