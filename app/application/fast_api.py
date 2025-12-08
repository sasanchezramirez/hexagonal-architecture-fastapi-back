
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.application.container import Container
from app.application.handler import Handlers
from typing import Final

from app.domain.model.util.exceptions import (
    DomainException,
    UserNotFoundException,
    DuplicateUserException,
    InvalidCredentialsException,
    InvalidTokenException,
    PersistenceException
)
from app.infrastructure.entry_point.utils.exception_handler import (
    domain_exception_handler,
    user_not_found_exception_handler,
    duplicate_user_exception_handler,
    invalid_credentials_exception_handler,
    token_exception_handler,
    persistence_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)


from app.application.logging_config import configure_logging

def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application with its dependencies, routes, and exception handlers.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Configure logging
    configure_logging()

    container: Final[Container] = Container()
    app: Final[FastAPI] = FastAPI(
        title="Hexagonal Architecture FastAPI Backend",
        description="REST API implemented with FastAPI and hexagonal architecture",
        version="1.0.0"
    )
    
    app.container = container
    
    # Register exception handlers
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    app.add_exception_handler(DuplicateUserException, duplicate_user_exception_handler)
    app.add_exception_handler(InvalidCredentialsException, invalid_credentials_exception_handler)
    app.add_exception_handler(InvalidTokenException, token_exception_handler) # Captures Invalid and Expired
    app.add_exception_handler(PersistenceException, persistence_exception_handler)
    app.add_exception_handler(DomainException, domain_exception_handler) # Domain fallback
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler) # Generic fallback

    # Include routers
    for handler in Handlers.iterator():
        app.include_router(handler.router)
        
    return app
