import logging
from typing import Final, Optional

from datetime import datetime
from app.domain.model.user import User
from app.domain.model.util.custom_exceptions import CustomException
from app.domain.model.util.response_codes import ResponseCodeEnum
from app.domain.gateway.persistence_gateway import PersistenceGateway
from app.domain.usecase.util.security import verify_password
from app.domain.usecase.util.jwt import create_access_token


logger: Final[logging.Logger] = logging.getLogger("Auth UseCase")


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

        Args:
            persistence_gateway: Gateway para operaciones de persistencia
        """
        self.persistence_gateway: Final[PersistenceGateway] = persistence_gateway

    def authenticate_user(self, user: User) -> Optional[str]:
        """
        Autentica un usuario y genera un token de acceso si las credenciales son válidas.

        Args:
            user: Usuario a autenticar con sus credenciales

        Returns:
            Optional[str]: Token de acceso si la autenticación es exitosa, None en caso contrario
        """
        try:
            user_validated = self.get_user(user)
            if user and verify_password(user.password, user_validated.password):
                return create_access_token({"sub": user.email})
            return None
        except CustomException as e:
            logger.error(f"Error de autenticación: {e}")
            raise
        except Exception as e:
            logger.error(f"Error no manejado en autenticación: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)

    def get_user(self, user_to_get: User) -> User:
        """
        Obtiene un usuario por su correo electrónico.

        Args:
            user_to_get: Usuario con el correo electrónico a buscar

        Returns:
            User: Usuario encontrado

        Raises:
            CustomException: Si hay un error al obtener el usuario
        """
        logger.info("Iniciando búsqueda de usuario por correo electrónico")
        try:
            return self.persistence_gateway.get_user_by_email(user_to_get.email)
        except CustomException as e:
            logger.error(f"Error al obtener usuario: {e}")
            raise
        except Exception as e:
            logger.error(f"Error no manejado al obtener usuario: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)



            

