from abc import ABC, abstractmethod
from typing import Optional

from app.domain.model.user import User


class IUserDataGateway(ABC):
    """
    This interface defines the necessary methods to get the users data.
    It is an async and abstract interface.
    """

    @abstractmethod
    async def create_user(self, user: User) -> User:
        """
        Creates a new user in the persistence layer.

        Args:
            user: The user entity to create.

        Returns:
            User: The created user with an assigned ID.

        Raises:
            CustomException: If an error occurs while creating the user.
        """
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            Optional[User]: The found user or None if they do not exist.

        Raises:
            CustomException: If an error occurs while retrieving the user.
        """
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user by their email address.

        Args:
            email: The email address of the user to retrieve.

        Returns:
            Optional[User]: The found user or None if they do not exist.

        Raises:
            CustomException: If an error occurs while retrieving the user.
        """
        pass

    @abstractmethod
    async def update_user(self, user: User) -> User:
        """
        Updates an existing user's data.

        Args:
            user: The user entity with the data to be updated.

        Returns:
            User: The updated user.

        Raises:
            CustomException: If an error occurs while updating the user.
        """
        pass
