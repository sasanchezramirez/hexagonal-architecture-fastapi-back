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
    PersistenceException
)

logger = logging.getLogger("ExceptionHandler")

async def domain_exception_handler(request: Request, exc: DomainException):
    """Base handler for unspecified domain exceptions."""
    logger.warning(f"Caught unhandled domain exception: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )

async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    """Handler for UserNotFoundException (HTTP 404)."""
    logger.info(f"User resource not found: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )

async def duplicate_user_exception_handler(request: Request, exc: DuplicateUserException):
    """Handler for DuplicateUserException (HTTP 409)."""
    logger.info(f"Attempt to create duplicate user: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message},
    )

async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    """Handler for invalid credentials (HTTP 401)."""
    logger.info("Authentication attempt with invalid credentials.")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )

async def token_exception_handler(request: Request, exc: InvalidTokenException):
    """Handler for invalid or expired tokens (HTTP 401)."""
    logger.info(f"Authentication token error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
        headers={"WWW-Authenticate": "Bearer"},
    )

async def persistence_exception_handler(request: Request, exc: PersistenceException):
    """Handler for generic persistence layer errors (HTTP 500)."""
    logger.error(f"Unexpected persistence error: {exc.message}", exc_info=exc.original_exception)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred on the server."},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for Pydantic validation errors (HTTP 422)."""
    error_messages = [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
    logger.info(f"Request validation error: {error_messages}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "The request is invalid.", "errors": error_messages},
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Generic handler for any other unhandled exception (HTTP 500)."""
    logger.critical(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal error occurred."},
    )
