import logging
from typing import Final, Optional
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

    def get_user(self, user: User) -> User:
        """
        Obtiene un usuario por su ID o email.
        Si se proporciona el email, se busca por email.
        Si el email está vacío, se busca por ID.
        Si se proporcionan ambos, se prioriza la búsqueda por email.

        Args:
            user: Usuario con ID o email para buscar

        Returns:
            User: Usuario encontrado

        Raises:
            CustomException: Si el usuario no existe o hay un error
        """
        logger.info("Iniciando obtención de usuario")
        try:
            # Si se proporciona el email, buscar por email
            if user.email and user.email != "default@example.com":
                logger.info(f"Buscando usuario por email: {user.email}")
                return self.persistence_gateway.get_user_by_email(user.email)
            
            # Si no hay email o está vacío, buscar por ID
            if user.id:
                logger.info(f"Buscando usuario por ID: {user.id}")
                return self.persistence_gateway.get_user_by_id(user.id)
            
            # Si no hay ni email ni ID, lanzar error
            logger.error("No se proporcionó ni email ni ID para la búsqueda")
            raise CustomException(ResponseCodeEnum.KOU02)
            
        except CustomException as e:
            logger.error(f"Error al obtener usuario: {e}")
            raise
        except Exception as e:
            logger.error(f"Error no manejado al obtener usuario: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)

    def update_user(self, user: User) -> User:
        """
        Actualiza un usuario existente.

        Args:
            user: Usuario con los datos a actualizar

        Returns:
            User: Usuario actualizado

        Raises:
            CustomException: Si el usuario no existe o hay un error
        """
        logger.info("Iniciando actualización de usuario")
        try:
            # Solo hashear el password si se proporciona uno nuevo
            if user.password is not None:
                logger.info("Actualizando contraseña del usuario")
                user.password = hash_password(user.password)
            else:
                logger.info("No se actualizará la contraseña del usuario")
            
            return self.persistence_gateway.update_user(user)
        except CustomException as e:
            logger.error(f"Error al actualizar usuario: {e}")
            raise
        except Exception as e:
            logger.error(f"Error no manejado al actualizar usuario: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)




            

