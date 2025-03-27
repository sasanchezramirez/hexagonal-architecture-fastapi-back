import logging
from typing import Final
from datetime import datetime

from app.domain.model.user import User
from app.domain.model.util.custom_exceptions import CustomException
from app.domain.model.util.response_codes import ResponseCodeEnum
from app.domain.gateway.persistence_gateway import PersistenceGateway
from app.domain.usecase.util.security import hash_password


logger: Final[logging.Logger] = logging.getLogger("User UseCase")


class UserUseCase:
    """
    Caso de uso para la gestión de usuarios.
    
    Esta clase maneja la lógica de negocio relacionada con las operaciones
    CRUD de usuarios, incluyendo la creación, lectura, actualización y
    el manejo seguro de contraseñas.
    """

    def __init__(self, persistence_gateway: PersistenceGateway) -> None:
        """
        Inicializa el caso de uso de usuario.

        Args:
            persistence_gateway: Gateway para operaciones de persistencia
        """
        self.persistence_gateway: Final[PersistenceGateway] = persistence_gateway

    def create_user(self, user: User) -> User:
        """
        Crea un nuevo usuario en el sistema.

        Args:
            user: Usuario a crear

        Returns:
            User: Usuario creado con ID asignado

        Raises:
            CustomException: Si hay un error al crear el usuario
        """
        logger.info("Iniciando creación de usuario")
        try:
            user.creation_date = datetime.now().isoformat()
            user.password = hash_password(user.password)
            return self.persistence_gateway.create_user(user)
        except CustomException as e:
            logger.error(f"Error al crear usuario: {e}")
            raise
        except Exception as e:
            logger.error(f"Error no manejado al crear usuario: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)

    def get_user(self, user_to_get: User) -> User:
        """
        Obtiene un usuario por su ID o correo electrónico.

        Args:
            user_to_get: Usuario con ID o correo electrónico a buscar

        Returns:
            User: Usuario encontrado

        Raises:
            CustomException: Si hay un error al obtener el usuario
        """
        logger.info("Iniciando búsqueda de usuario")
        try:
            if user_to_get.id and user_to_get.id != 0:
                return self.persistence_gateway.get_user_by_id(user_to_get.id)
            return self.persistence_gateway.get_user_by_email(user_to_get.email)
        except CustomException as e:
            logger.error(f"Error al obtener usuario: {e}")
            raise
        except Exception as e:
            logger.error(f"Error no manejado al obtener usuario: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)

    def update_user(self, user: User) -> User:
        """
        Actualiza los datos de un usuario existente.

        Args:
            user: Usuario con los datos a actualizar

        Returns:
            User: Usuario actualizado

        Raises:
            CustomException: Si hay un error al actualizar el usuario
        """
        logger.info("Iniciando actualización de usuario")
        try:
            if user.password:
                user.password = hash_password(user.password)
            return self.persistence_gateway.update_user(user)
        except CustomException as e:
            logger.error(f"Error al actualizar usuario: {e}")
            raise
        except Exception as e:
            logger.error(f"Error no manejado al actualizar usuario: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)




            

