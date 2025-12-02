import logging
from typing import Final
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.domain.gateway.user_data_gateway import IUserDataGateway
from app.domain.model.util.exceptions import UserNotFoundException, DuplicateUserException, PersistenceException
from app.infrastructure.driven_adapter.persistence.user_repository.sqlalchemy_user_repository import UserRepository
from app.domain.model.user import User
from app.infrastructure.driven_adapter.persistence.user_repository.user_mapper import UserMapper

logger: Final = logging.getLogger(__name__)

class UserDataGatewayImpl(IUserDataGateway):
    """
    Implementation of the User Data Gateway.
    
    This class acts as an adapter between the domain layer and the persistence layer,
    handling data conversion and exception mapping.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the user data gateway implementation.
        
        Args:
            userRepository: The user repository for database operations.
        """
        self.user_repository = user_repository
        
    async def create_user(self, user: User) -> User:
        """
        Creates a new user in the database.
        """
        user_entity = UserMapper.to_entity(user)

        try:
            saved_entity = await self.user_repository.create_user(user_entity)
            return UserMapper.to_domain(saved_entity)
        except IntegrityError: 
            raise DuplicateUserException(f"The user with email {user.email} is already in use by another user.")
        except SQLAlchemyError as e:
            raise PersistenceException(f"Database error during creation: {e}")


    async def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieves a user by their ID.
        """
        entity = await self.user_repository.get_user_by_id(user_id)

        if not entity:
            return None
            
        return UserMapper.to_domain(entity)

    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a user by their email.
        """
        entity = await self.user_repository.get_by_email(email)
        
        if not entity:
            return None
            
        return UserMapper.to_domain(entity)
    
    async def update_user(self, user: User) -> User:
        """
        Updates an existing user.
        """
        if user.id is None:
            raise ValueError("User ID cannot be None for update")

        existing_entity = await self.user_repository.get_user_by_id(user.id)
        if not existing_entity:
            raise UserNotFoundException(f"User with id {user.id} not found")

        entity_to_update = UserMapper.to_entity(user)
        
        try:
            updated_entity = await self.user_repository.update(entity_to_update)
            
            return UserMapper.to_domain(updated_entity)

        except IntegrityError:
            raise DuplicateUserException(f"The email {user.email} is already in use by another user.")
            
        except SQLAlchemyError as e:
            raise PersistenceException(f"Database error during update: {e}")

