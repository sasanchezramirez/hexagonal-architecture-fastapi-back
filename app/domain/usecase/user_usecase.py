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
        user.creation_date = datetime.now().isoformat()
        user.password = hash_password(user.password)
        return await self.persistence_gateway.create_user(user)

    async def get_user(self, user: User) -> User:
        """
        Obtiene un usuario por su ID o email.
        """
        logger.info(f"Iniciando obtención de usuario por ID: {user.id} o Email: {user.email}")
        
        found_user: Optional[User] = None
        if user.email and user.email != "default@example.com":
            found_user = await self.persistence_gateway.get_user_by_email(user.email)
        elif user.id:
            found_user = await self.persistence_gateway.get_user_by_id(user.id)

        if not found_user:
            raise UserNotFoundException(user_id=user.id, email=user.email)
            
        return found_user

    async def update_user(self, user: User) -> User:
        """
        Actualiza un usuario existente.
        """
        logger.info(f"Iniciando actualización de usuario con ID: {user.id}")
        
        if user.password:
            logger.info("Actualizando contraseña del usuario.")
            user.password = hash_password(user.password)
        
        return await self.persistence_gateway.update_user(user)




            

