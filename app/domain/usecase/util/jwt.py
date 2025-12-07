import jwt
import logging

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from datetime import datetime, timedelta
from app.application.settings import settings
from app.domain.model.util.exceptions import ExpiredTokenException, InvalidTokenException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

logger = logging.getLogger("SecurityValidations")


def create_access_token(data: dict) -> str:
    """Creates a new JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """
    Verifies a JWT token and returns its payload if valid.
    
    Raises:
        ExpiredTokenException: If the token has expired.
        InvalidTokenException: If the token is invalid for any other reason.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("The authentication token has expired.")
        raise ExpiredTokenException()
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        raise InvalidTokenException()
    
async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    FastAPI dependency to get the current user from a token.
    Verifies the token and returns the payload.
    """
    payload = verify_token(token)
    return payload
