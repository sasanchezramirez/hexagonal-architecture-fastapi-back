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
    Use case for user management.
    
    This class handles business logic related to user CRUD operations,
    including creation, reading, updating, and secure password handling.
    """

    def __init__(self, user_data_gateway: IUserDataGateway) -> None:
        """
        Initializes the user use case.
        """
        self.user_data_gateway: Final[IUserDataGateway] = user_data_gateway

    async def create_user(self, user: User) -> User:
        """
        Creates a new user in the system.
        """
        logger.info(f"Starting user creation for email: {user.email}")
        user.creation_date = datetime.now().isoformat()
        user.password = hash_password(user.password)
        return await self.user_data_gateway.create_user(user)

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieves a user by their ID.
        """
        logger.info(f"Starting user retrieval by ID: {user_id}")
        user = await self.user_data_gateway.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id=user_id)
        return user

    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a user by their email.
        """
        logger.info(f"Starting user retrieval by email: {email}")
        user = await self.user_data_gateway.get_user_by_email(email)
        
        if not user:
            raise UserNotFoundException(email=email)
        return user

    async def update_user(self, user: User) -> User:
        """
        Updates an existing user.
        """
        logger.info(f"Starting user update with ID: {user.id}")
        
        if user.password:
            logger.info("Updating user password.")
            user.password = hash_password(user.password)
        
        return await self.user_data_gateway.update_user(user)




            

