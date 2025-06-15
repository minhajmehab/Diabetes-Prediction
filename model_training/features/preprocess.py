import logging
from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

def preprocess_data(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Splits the input DataFrame into train and test sets for features and target.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing features and target.
    test_size : float, optional
        Proportion of the dataset to include in the test split (default is 0.2).
    random_state : int, optional
        Random seed for reproducibility (default is 42).

    Returns
    -------
    X_train : pd.DataFrame
        Training features.
    X_test : pd.DataFrame
        Testing features.
    y_train : pd.Series
        Training target.
    y_test : pd.Series
        Testing target.

    Raises
    ------
    ValueError
        If required columns are missing in the DataFrame.
    """
    required_columns = {'Outcome', 'Id'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        logger.error(f"Missing columns in DataFrame: {missing}")
        raise ValueError(f"Missing columns in DataFrame: {missing}")

    X = df.drop(['Outcome', 'Id'], axis=1)
    y = df['Outcome']

    logger.info("Splitting data into train and test sets.")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )
    logger.info(
        f"Data split complete: "
        f"X_train: {X_train.shape}, X_test: {X_test.shape}, "
        f"y_train: {y_train.shape}, y_test: {y_test.shape}"
    )
    return X_train, X_test, y_train, y_test
