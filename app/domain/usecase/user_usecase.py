import logging
from typing import Final
from datetime import datetime

from app.domain.model.user import User
from app.domain.model.util.exceptions import UserNotFoundException
from app.domain.gateway.user_data_gateway import IUserDataGateway
from app.domain.usecase.util.security import hash_password


logger: Final[logging.Logger] = logging.getLogger("UserUseCase")


class UserUseCase:
    """
    Caso de uso para la gestión de usuarios.
    
    Esta clase maneja la lógica de negocio relacionada con las operaciones
    CRUD de usuarios, incluyendo la creación, lectura, actualización y
    el manejo seguro de contraseñas.
    """

    def __init__(self, user_data_gateway: IUserDataGateway) -> None:
        """
        Inicializa el caso de uso de usuario.
        """
        self.user_data_gateway: Final[IUserDataGateway] = user_data_gateway

    async def create_user(self, user: User) -> User:
        """
        Crea un nuevo usuario en el sistema.
        """
        logger.info(f"Iniciando creación de usuario para el email: {user.email}")
        user.creation_date = datetime.now().isoformat()
        user.password = hash_password(user.password)
        return await self.user_data_gateway.create_user(user)

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Obtiene un usuario por su ID.
        """
        logger.info(f"Iniciando obtención de usuario por ID: {user_id}")
        user = await self.user_data_gateway.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)
        return user

    async def get_user_by_email(self, email: str) -> User:
        """
        Obtiene un usuario por su email.
        """
        logger.info(f"Iniciando obtención de usuario por email: {email}")
        user = await self.user_data_gateway.get_user_by_email(email)
        
        if not user:
            raise UserNotFoundException(email=email)
        return user

    async def update_user(self, user: User) -> User:
        """
        Actualiza un usuario existente.
        """
        logger.info(f"Iniciando actualización de usuario con ID: {user.id}")
        
        if user.password:
            logger.info("Actualizando contraseña del usuario.")
            user.password = hash_password(user.password)
        
        return await self.user_data_gateway.update_user(user)




            

