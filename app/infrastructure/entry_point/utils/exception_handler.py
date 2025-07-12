import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.domain.model.util.exceptions import (
    DomainException,
    UserNotFoundException,
    DuplicateUserException,
    InvalidCredentialsException,
    InvalidTokenException,
    ExpiredTokenException,
    PersistenceException
)

logger = logging.getLogger("ExceptionHandler")

async def domain_exception_handler(request: Request, exc: DomainException):
    """Manejador base para excepciones de dominio no especificadas."""
    logger.warning(f"Se capturó una excepción de dominio no manejada: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )

async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    """Manejador para la excepción UserNotFoundException (HTTP 404)."""
    logger.info(f"Recurso de usuario no encontrado: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )

async def duplicate_user_exception_handler(request: Request, exc: DuplicateUserException):
    """Manejador para la excepción DuplicateUserException (HTTP 409)."""
    logger.info(f"Intento de crear un usuario duplicado: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message},
    )

async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    """Manejador para credenciales inválidas (HTTP 401)."""
    logger.info(f"Intento de autenticación con credenciales inválidas.")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )

async def token_exception_handler(request: Request, exc: InvalidTokenException):
    """Manejador para tokens inválidos o expirados (HTTP 401)."""
    logger.info(f"Error de token de autenticación: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )

async def persistence_exception_handler(request: Request, exc: PersistenceException):
    """Manejador para errores genéricos de la capa de persistencia (HTTP 500)."""
    logger.error(f"Error inesperado de persistencia: {exc.message}", exc_info=exc.original_exception)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ocurrió un error inesperado en el servidor."},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejador para errores de validación de Pydantic (HTTP 422)."""
    error_messages = [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
    logger.info(f"Error de validación de la petición: {error_messages}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "La petición no es válida.", "errors": error_messages},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Manejador genérico para cualquier otra excepción no controlada (HTTP 500)."""
    logger.critical(f"Excepción no controlada: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Ocurrió un error interno inesperado."},
    )
