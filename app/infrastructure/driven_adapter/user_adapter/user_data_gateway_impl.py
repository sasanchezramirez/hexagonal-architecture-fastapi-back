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

    def __init__(self, userRepository: UserRepository):
        self.user_repository = userRepository
        
    async def create_user(self, user: User) -> User:

        user_entity = UserMapper.to_entity(user)

        try:
            saved_entity = await self.user_repository.create_user(user_entity)
            return UserMapper.to_domain(saved_entity)
        except IntegrityError: 
            raise DuplicateUserException(f"The user with email {user.email} is already in use by another user.")
        except SQLAlchemyError as e:
            raise PersistenceException(f"Database error during update: {e}")


    async def get_user_by_id(self, user_id: int) -> User:

        entity = await self.repository.get_user_by_id(user_id)

        if not entity:
            return None
            
        return UserMapper.to_domain(entity)

    async def get_user_by_email(self, email: str) -> User:
        entity = await self.repository.get_user_by_email(email)
        
        if not entity:
            return None
            
        return UserMapper.to_domain(entity)
    
    async def update_user(self, user: User) -> User:
        if user.id is None:
            raise ValueError("User ID cannot be None for update")

        existing_entity = await self.repository.get_user_by_id(user.id)
        if not existing_entity:
            raise UserNotFoundException(f"User with id {user.id} not found")

        entity_to_update = UserMapper.to_entity(user)
        
        try:
            updated_entity = await self.repository.update(entity_to_update)
            
            return UserMapper.to_domain(updated_entity)

        except IntegrityError:
            raise DuplicateUserException(f"The email {user.email} is already in use by another user.")
            
        except SQLAlchemyError as e:
            raise PersistenceException(f"Database error during update: {e}")

