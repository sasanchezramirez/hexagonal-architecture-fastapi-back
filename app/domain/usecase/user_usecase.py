import logging
from typing import Final, Optional
from datetime import datetime

from app.domain.model.user import User
from app.domain.model.util.exceptions import UserNotFoundException
from app.domain.gateway.persistence_gateway import PersistenceGateway
from app.domain.usecase.util.security import hash_password


logger: Final[logging.Logger] = logging.getLogger("UserUseCase")


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
        """
        self.persistence_gateway: Final[PersistenceGateway] = persistence_gateway

    async def create_user(self, user: User) -> User:
        """
        Crea un nuevo usuario en el sistema.
        """
        logger.info(f"Iniciando creación de usuario para el email: {user.email}")
        # La lógica de negocio aquí es hashear la contraseña y establecer la fecha.
        user.creation_date = datetime.now().isoformat()
        user.password = hash_password(user.password)
        
        # Delegar la creación a la capa de persistencia.
        # Si el usuario ya existe, el gateway lanzará DuplicateUserException.
        return await self.persistence_gateway.create_user(user)

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Obtiene un usuario por su ID.
        """
        logger.info(f"Iniciando obtención de usuario por ID: {user_id}")
        user = await self.persistence_gateway.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)
        return user

    async def get_user_by_email(self, email: str) -> User:
        """
        Obtiene un usuario por su email.
        """
        logger.info(f"Iniciando obtención de usuario por email: {email}")
        user = await self.persistence_gateway.get_user_by_email(email)
        if not user:
            raise UserNotFoundException(email=email)
        return user

    async def update_user(self, user: User) -> User:
        """
        Actualiza un usuario existente.
        """
        logger.info(f"Iniciando actualización de usuario con ID: {user.id}")
        
        # Lógica de negocio: solo hashear el password si se proporciona uno nuevo.
        if user.password:
            logger.info("Actualizando contraseña del usuario.")
            user.password = hash_password(user.password)
        
        # Delegar la actualización.
        # Si el usuario no existe, el gateway lanzará UserNotFoundException.
        return await self.persistence_gateway.update_user(user)




            

