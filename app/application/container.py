from typing import Final

from dependency_injector import containers, providers

from app.application.handler import Handlers
from app.domain.usecase.user_usecase import UserUseCase
from app.domain.usecase.auth_usecase import AuthUseCase
from app.infrastructure.driven_adapter.persistence.service.persistence import Persistence
from app.infrastructure.driven_adapter.persistence.config.database import SessionLocal


class Container(containers.DeclarativeContainer):
    """
    Contenedor de inyección de dependencias.
    
    Esta clase configura y proporciona todas las dependencias
    necesarias para la aplicación, siguiendo el principio de
    inversión de dependencias.
    """

    # Configuración de inyección de dependencias
    wiring_config: Final = containers.WiringConfiguration(
        modules=Handlers.get_module_namespaces()
    )

    # Sesión de base de datos
    session: Final = providers.Singleton(SessionLocal)

    # Gateway de persistencia
    persistence_gateway: Final = providers.Factory(
        Persistence,
        session=session
    )

    # Casos de uso
    user_usecase: Final = providers.Factory(
        UserUseCase,
        persistence_gateway=persistence_gateway
    )
    
    auth_usecase: Final = providers.Factory(
        AuthUseCase,
        persistence_gateway=persistence_gateway
    )

