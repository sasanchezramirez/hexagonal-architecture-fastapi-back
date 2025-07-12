import logging
from typing import Final, Optional

from app.domain.model.user import User
from app.domain.model.util.exceptions import UserNotFoundException, InvalidCredentialsException
from app.domain.gateway.persistence_gateway import PersistenceGateway
from app.domain.usecase.util.security import verify_password
from app.domain.usecase.util.jwt import create_access_token


logger: Final[logging.Logger] = logging.getLogger("AuthUseCase")


class AuthUseCase:
    """
    Caso de uso para la autenticación de usuarios.
    
    Esta clase maneja la lógica de negocio relacionada con la autenticación
    de usuarios, incluyendo la verificación de credenciales y la generación
    de tokens de acceso.
    """

    def __init__(self, persistence_gateway: PersistenceGateway) -> None:
        """
        Inicializa el caso de uso de autenticación.
        """
        self.persistence_gateway: Final[PersistenceGateway] = persistence_gateway

    async def authenticate_user(self, user: User) -> str:
        """
        Autentica un usuario y genera un token de acceso si las credenciales son válidas.

        Args:
            user: Usuario a autenticar con sus credenciales.

        Returns:
            str: Token de acceso si la autenticación es exitosa.
        
        Raises:
            InvalidCredentialsException: Si el email no se encuentra o la contraseña es incorrecta.
        """
        logger.info(f"Iniciando autenticación para el usuario: {user.email}")
        
        db_user = await self.persistence_gateway.get_user_by_email(user.email)
        
        if not db_user or not verify_password(user.password, db_user.password):
            logger.warning(f"Intento de autenticación fallido para: {user.email}")
            raise InvalidCredentialsException()
            
        logger.info(f"Autenticación exitosa para: {user.email}")
        return create_access_token({"sub": db_user.email})



            

