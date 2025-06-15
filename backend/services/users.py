import logging

# ------------------ Logging Setup ------------------
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ------------------ Fake In-Memory User Database ------------------
# TODO: Replace with actual hashed-password database in production
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": "testpass",  # WARNING: Do not store plaintext passwords in production!
    }
}


def get_user(username: str) -> dict | None:
    """
    Retrieve a user from the fake database by username.

    Args:
        username (str): The username to look up.

    Returns:
        dict or None: User dictionary if found, else None.
    """
    return fake_users_db.get(username)


def authenticate_user(username: str, password: str) -> dict | None:
    """
    Validate the user's credentials.

    Args:
        username (str): Input username.
        password (str): Input password.

    Returns:
        dict or None: User dictionary if authentication succeeds, else None.
    """
    user = get_user(username)
    if not user:
        logger.warning(f"Authentication failed: user '{username}' not found.")
        return None

    if user["password"] != password:
        logger.warning(f"Authentication failed: incorrect password for user '{username}'.")
        return None

    logger.info(f"User '{username}' authenticated successfully.")
    return user
