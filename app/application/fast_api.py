from fastapi import FastAPI
from app.application.container import Container
from app.application.handler import Handlers
from typing import Final


def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI con sus dependencias y rutas.
    
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
    
    for handler in Handlers.iterator():
        app.include_router(handler.router)
        
    return app