from typing import Final

from dependency_injector import containers, providers

from app.application.handler import Handlers

from app.domain.usecase.user_usecase import UserUseCase
from app.domain.usecase.auth_usecase import AuthUseCase

from app.infrastructure.driven_adapter.persistence.config.database import AsyncSessionLocal
from app.infrastructure.driven_adapter.persistence.user_repository.sqlalchemy_user_repository import UserRepository
from app.infrastructure.driven_adapter.user_adapter.user_data_gateway_impl import UserDataGatewayImpl
from app.infrastructure.entry_point.handler.auth_handler import AuthHandler

class Container(containers.DeclarativeContainer):
    """
    Dependency injection container.
    
    This class configures and provides all dependencies
    required for the application, following the dependency
    inversion principle.
    """

    # Dependency injection configuration
    wiring_config: Final = containers.WiringConfiguration(
        modules=Handlers.get_module_namespaces()
    )

    # Async database session factory
    session_factory: Final = providers.Object(AsyncSessionLocal)

    # Persistence gateway
    user_repository: Final = providers.Factory(
        UserRepository,
        session_factory=session_factory
    )

    user_data_gateway: Final = providers.Factory(
        UserDataGatewayImpl,
        user_repository=user_repository
    )

    # Use cases
    user_usecase: Final = providers.Factory(
        UserUseCase,
        user_data_gateway=user_data_gateway
    )
    
    auth_usecase: Final = providers.Factory(
        AuthUseCase,
        user_data_gateway=user_data_gateway
    )

    # Handlers
    auth_handler: Final = providers.Factory(
        AuthHandler,
        user_usecase=user_usecase,
        auth_usecase=auth_usecase
    )

