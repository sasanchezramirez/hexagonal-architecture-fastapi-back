from typing import Final

from dependency_injector import containers, providers

from app.application.handler import Handlers

from app.domain.usecase.user_usecase import UserUseCase
from app.domain.usecase.auth_usecase import AuthUseCase

from app.infrastructure.driven_adapter.persistence.config.database import get_session
from app.infrastructure.driven_adapter.persistence.user_repository.sqlalchemy_user_repository import UserRepository
from app.infrastructure.driven_adapter.user_adapter.user_data_gateway_impl import UserDataGatewayImpl

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

    # Sesión de base de datos asíncrona
    session: Final = providers.Resource(get_session)

    # Gateway de persistencia
    user_repository: Final = providers.Factory(
        UserRepository,
        session=session
    )

    user_data_gateway: Final = providers.Factory(
        UserDataGatewayImpl,
        user_repository=user_repository
    )

    # Casos de uso
    user_usecase: Final = providers.Factory(
        UserUseCase,
        user_data_gateway=user_data_gateway
    )
    
    auth_usecase: Final = providers.Factory(
        AuthUseCase,
        user_data_gateway=user_data_gateway
    )

