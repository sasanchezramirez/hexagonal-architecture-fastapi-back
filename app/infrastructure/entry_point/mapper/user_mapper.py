

from datetime import datetime
from app.domain.model.user import User
from app.infrastructure.entry_point.dto.user_dto import (
    NewUserInput,
    GetUser,
    UserOutput,
    LoginInput,
    UpdateUserInput
)


def map_user_dto_to_user(user_dto: NewUserInput) -> User:
    """
    Maps a new user DTO to a domain model.

    Args:
        user_dto: DTO with new user data

    Returns:
        User: User domain model
    """
    return User(
        email=user_dto.email,
        password=user_dto.password,
        profile_id=user_dto.profile_id,
        status_id=user_dto.status_id,
        creation_date=datetime.now().isoformat()
    )


def map_user_to_user_output_dto(user: User) -> UserOutput:
    """
    Maps a domain model to an output DTO.

    Args:
        user: User domain model

    Returns:
        UserOutput: DTO with user data
    """
    return UserOutput(
        id=user.id,
        email=user.email,
        creation_date=user.creation_date,
        profile_id=user.profile_id,
        status_id=user.status_id
    )


def map_get_user_dto_to_user(user_dto: GetUser) -> User:
    """
    Maps a search DTO to a domain model.

    Args:
        user_dto: DTO with search criteria

    Returns:
        User: User domain model
    """
    # If no email, use a default email for validation
    # The real email will be handled in the use case
    email = user_dto.email if user_dto.email else "default@example.com"
    
    return User(
        id=user_dto.id,
        email=email,
        creation_date=datetime.now().isoformat()  # Default date for search
    )


def map_login_dto_to_user(user_dto: LoginInput) -> User:
    """
    Maps a login DTO to a domain model.

    Args:
        user_dto: DTO with login credentials

    Returns:
        User: User domain model
    """
    return User(
        email=user_dto.email,
        password=user_dto.password,
        creation_date=datetime.now().isoformat()  # Default date for login
    )


def map_update_user_dto_to_user(user_dto: UpdateUserInput) -> User:
    """
    Maps an update DTO to a domain model.

    Args:
        user_dto: DTO with data to update

    Returns:
        User: User domain model
    """
    # Create dictionary with base fields
    user_data = {
        "id": user_dto.id,
        "email": user_dto.email,
        "profile_id": user_dto.profile_id,
        "status_id": user_dto.status_id,
        "creation_date": datetime.now().isoformat()  # Default date for update
    }
    
    # Only add password if not None
    if user_dto.password is not None:
        user_data["password"] = user_dto.password
    
    return User(**user_data)