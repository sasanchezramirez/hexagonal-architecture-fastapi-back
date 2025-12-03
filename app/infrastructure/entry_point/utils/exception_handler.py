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

def _create_error_response(status_code: int, message: str, data: dict = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "apiCode": str(status_code),
            "data": data,
            "message": message,
            "status": False
        },
    )

async def domain_exception_handler(request: Request, exc: DomainException):
    """Base handler for unspecified domain exceptions."""
    logger.warning(f"Caught unhandled domain exception: {exc.message}")
    return _create_error_response(status.HTTP_400_BAD_REQUEST, exc.message)

async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    """Handler for UserNotFoundException (HTTP 404)."""
    logger.info(f"User resource not found: {exc.message}")
    return _create_error_response(status.HTTP_404_NOT_FOUND, exc.message)

async def duplicate_user_exception_handler(request: Request, exc: DuplicateUserException):
    """Handler for DuplicateUserException (HTTP 409)."""
    logger.info(f"Attempt to create duplicate user: {exc.message}")
    return _create_error_response(status.HTTP_409_CONFLICT, exc.message)

async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    """Handler for invalid credentials (HTTP 401)."""
    logger.info("Authentication attempt with invalid credentials.")
    response = _create_error_response(status.HTTP_401_UNAUTHORIZED, exc.message)
    response.headers["WWW-Authenticate"] = "Bearer"
    return response

async def token_exception_handler(request: Request, exc: InvalidTokenException):
    """Handler for invalid or expired tokens (HTTP 401)."""
    logger.info(f"Authentication token error: {exc.message}")
    response = _create_error_response(status.HTTP_401_UNAUTHORIZED, exc.message)
    response.headers["WWW-Authenticate"] = "Bearer"
    return response

async def persistence_exception_handler(request: Request, exc: PersistenceException):
    """Handler for generic persistence layer errors (HTTP 500)."""
    logger.error(f"Unexpected persistence error: {exc.message}", exc_info=exc.original_exception)
    return _create_error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "An unexpected error occurred on the server.")

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for Pydantic validation errors (HTTP 422)."""
    error_messages = [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
    logger.info(f"Request validation error: {error_messages}")
    return _create_error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY, 
        "The request is invalid.", 
        data={"errors": error_messages}
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Generic handler for any other unhandled exception (HTTP 500)."""
    logger.critical(f"Unhandled exception: {exc}", exc_info=True)
    return _create_error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "An unexpected internal error occurred.")
