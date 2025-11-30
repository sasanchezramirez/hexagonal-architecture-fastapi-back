import logging
from typing import Final, Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.future import select

from app.infrastructure.driven_adapter.persistence.entity.user_entity import UserEntity


logger: Final[logging.Logger] = logging.getLogger("UserRepository")


class UserRepository:
    """
    Data Access Layer (DAL) for the User entity.

    This class implements basic CRUD operations directly with the database
    for the UserEntity, using SQLAlchemy in asynchronous mode.
    Its responsibility is exclusively database interaction, without business logic
    or domain knowledge.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initializes the user repository.

        Args:
            session: Asynchronous SQLAlchemy session for database operations.
        """
        self.session: Final[AsyncSession] = session

    async def create_user(self, user_entity: UserEntity) -> UserEntity:
        """
        Creates a new user entity in the database.
        """
        try:
            self.session.add(user_entity)
            await self.session.flush()  # Flush to get the ID and check constraints
            await self.session.refresh(user_entity)
            return user_entity
        except IntegrityError as e:
            logger.error(f"Integrity error while creating user: {e}")
            raise e
        except SQLAlchemyError as e:
            logger.error(f"Unknown database error: {e}")
            raise e

    async def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        """
        Retrieves a user entity by its ID.

        Note:
            This method intentionally omits a try-except block for 'not found' scenarios.
            If the user is not found, it returns None, which should be handled by the domain
            layer. Connection errors are allowed to propagate.
        """
        stmt = select(UserEntity).where(UserEntity.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[UserEntity]:
        """
        Retrieves a user entity by its email address.
        """
        stmt = select(UserEntity).where(UserEntity.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[UserEntity]:
        """
        Retrieves a list of user entities with pagination.

        Args:
            skip: Number of records to skip (offset). Defaults to 0.
            limit: Maximum number of records to return. Defaults to 100.

        Returns:
            List[UserEntity]: A list of user entities.
        """
        stmt = select(UserEntity).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, user_entity: UserEntity) -> UserEntity:
        """
        Updates an existing user entity.
        """
        try:
            updated_instance = await self.session.merge(user_entity)
            await self.session.flush()
            await self.session.refresh(updated_instance)
            return updated_instance
        except IntegrityError as e:
            raise e