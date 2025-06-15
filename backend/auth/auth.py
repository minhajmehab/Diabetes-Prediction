import logging
from datetime import datetime, timedelta

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from services.users import get_user

# ------------------ Logging Setup ------------------
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ------------------ Auth Config ------------------
SECRET_KEY = "your-secret-key"  # Change in production or load from env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"Access token created for data: {data}")
    return token


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            logger.warning("JWT 'sub' claim is missing.")
            raise credentials_exception

        user = get_user(username)

        if user is None:
            logger.warning(f"User not found: {username}")
            raise credentials_exception

        logger.debug(f"Authenticated user: {username}")
        return user

    except JWTError as e:
        logger.error(f"JWT decoding error: {e}")
        raise credentials_exception
