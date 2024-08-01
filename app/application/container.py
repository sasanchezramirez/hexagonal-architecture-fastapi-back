from  dependency_injector import containers, providers
from app.application.handler import Handlers
from app.domain.usecase.user_usecase import UserUseCase
# from app.domain.usecase.etl_usecase import EtlUseCase
# from app.infrastructure.driven_adapter.persistence.service.presistence import Persistence
# from app.infrastructure.driven_adapter.persistence.config.database import SessionLocal
# from app.infrastructure.driven_adapter.cognito.service.service import CognitoService
# from app.infrastructure.driven_adapter.kiire.service.service import KiireService

class Container(containers.DeclarativeContainer):

    #Cargo los handles donde esté @injects
    wiring_config = containers.WiringConfiguration(modules= Handlers.modules())

    # # Proveer sesiones de SQLAlchemy
    # session = providers.Singleton(SessionLocal)

    # # Registro de Gateway
    # persistence_gateway = providers.Factory(Persistence, session=session)
    # cognito_gateway = providers.Factory(CognitoService)
    # kiire_gateway = providers.Factory(KiireService)

    # # Cargo usecases
    # user_usecase = providers.Factory(UserUseCase, persistence_gateway=persistence_gateway, cognito_gateway=cognito_gateway)
    # etl_usecase = providers.Factory(EtlUseCase, persistence_gateway=persistence_gateway, kiire_gateway=kiire_gateway)

