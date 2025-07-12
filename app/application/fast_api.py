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


def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI con sus dependencias, rutas y manejadores de excepciones.
    
    Returns:
        FastAPI: Instancia configurada de la aplicación FastAPI
    """
    container: Final[Container] = Container()
    app: Final[FastAPI] = FastAPI(
        title="Hexagonal Architecture FastAPI Backend",
        description="API REST implementada con FastAPI y arquitectura hexagonal",
        version="1.0.0"
    )
    
    app.container = container
    
    # Registrar manejadores de excepciones
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    app.add_exception_handler(DuplicateUserException, duplicate_user_exception_handler)
    app.add_exception_handler(InvalidCredentialsException, invalid_credentials_exception_handler)
    app.add_exception_handler(InvalidTokenException, token_exception_handler) # Captura Invalid y Expired
    app.add_exception_handler(PersistenceException, persistence_exception_handler)
    app.add_exception_handler(DomainException, domain_exception_handler) # Fallback para dominio
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler) # Fallback genérico

    # Incluir routers
    for handler in Handlers.iterator():
        app.include_router(handler.router)
        
    return app
