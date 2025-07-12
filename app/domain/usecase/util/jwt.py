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
    """Crea un nuevo token de acceso JWT."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """
    Verifica un token JWT y devuelve su payload si es válido.
    
    Raises:
        ExpiredTokenException: Si el token ha expirado.
        InvalidTokenException: Si el token es inválido por cualquier otra razón.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("El token de autenticación ha expirado.")
        raise ExpiredTokenException()
    except jwt.InvalidTokenError as e:
        logger.error(f"Token inválido: {e}")
        raise InvalidTokenException()
    
async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependencia de FastAPI para obtener el usuario actual a partir de un token.
    Verifica el token y devuelve el payload.
    """
    payload = verify_token(token)
    return payload
