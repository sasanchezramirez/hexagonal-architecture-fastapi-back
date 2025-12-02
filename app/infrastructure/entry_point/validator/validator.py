import re

from app.infrastructure.entry_point.dto.user_dto import (
    NewUserInput,
    GetUser,
    LoginInput,
    UpdateUserInput
)


def is_valid_email(email: str) -> bool:
    """
    Validates email format more flexibly.
    
    Args:
        email: Email to validate
        
    Returns:
        bool: True if format is valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_new_user(user: NewUserInput) -> bool:
    """
    Validates new user data.

    Args:
        user: DTO with new user data

    Returns:
        bool: True if validation is successful

    Raises:
        ValueError: If data is invalid
    """
    if not user.email:
        raise ValueError("Email is required")
    
    if not is_valid_email(user.email):
        raise ValueError("Invalid email format")
    
    if not user.password or len(user.password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    if not user.profile_id or user.profile_id <= 0:
        raise ValueError("Profile ID must be greater than 0")
    
    if not user.status_id or user.status_id <= 0:
        raise ValueError("Status ID must be greater than 0")
    
    return True


def validate_get_user(user: GetUser) -> bool:
    """
    Validates user search criteria.

    Args:
        user: DTO with search criteria

    Returns:
        bool: True if validation is successful

    Raises:
        ValueError: If data is invalid
    """
    if not user.id and not user.email:
        raise ValueError("Must provide either ID or email")
    
    if user.email and not is_valid_email(user.email):
        raise ValueError("Invalid email format")
    
    return True


def validate_login(user: LoginInput) -> bool:
    """
    Validates login credentials.

    Args:
        user: DTO with login credentials

    Returns:
        bool: True if validation is successful

    Raises:
        ValueError: If data is invalid
    """
    if not user.email:
        raise ValueError("Email is required")
    
    if not is_valid_email(user.email):
        raise ValueError("Invalid email format")
    
    if not user.password or len(user.password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    return True


def validate_update_user(user: UpdateUserInput) -> bool:
    """
    Validates user update data.

    Args:
        user: DTO with data to update

    Returns:
        bool: True if validation is successful

    Raises:
        ValueError: If data is invalid
    """
    if not user.id or user.id <= 0:
        raise ValueError("User ID is required and must be greater than 0")
    
    if user.email and not is_valid_email(user.email):
        raise ValueError("Invalid email format")
    
    if user.password and len(user.password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    if user.profile_id is not None and user.profile_id <= 0:
        raise ValueError("Profile ID must be greater than 0")
    
    if user.status_id is not None and user.status_id <= 0:
        raise ValueError("Status ID must be greater than 0")
    
    return True
