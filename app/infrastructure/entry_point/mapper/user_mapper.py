from typing import Final

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
    Mapea un DTO de nuevo usuario a un modelo de dominio.

    Args:
        user_dto: DTO con los datos del nuevo usuario

    Returns:
        User: Modelo de dominio de usuario
    """
    return User(
        email=user_dto.email,
        password=user_dto.password,
        profile_id=user_dto.profile_id,
        status_id=user_dto.status_id,
    )


def map_user_to_user_output_dto(user: User) -> UserOutput:
    """
    Mapea un modelo de dominio a un DTO de salida.

    Args:
        user: Modelo de dominio de usuario

    Returns:
        UserOutput: DTO con los datos del usuario
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
    Mapea un DTO de búsqueda a un modelo de dominio.

    Args:
        user_dto: DTO con los criterios de búsqueda

    Returns:
        User: Modelo de dominio de usuario
    """
    return User(
        id=user_dto.id,
        email=user_dto.email
    )


def map_login_dto_to_user(user_dto: LoginInput) -> User:
    """
    Mapea un DTO de login a un modelo de dominio.

    Args:
        user_dto: DTO con las credenciales de login

    Returns:
        User: Modelo de dominio de usuario
    """
    return User(
        email=user_dto.email,
        password=user_dto.password
    )


def map_update_user_dto_to_user(user_dto: UpdateUserInput) -> User:
    """
    Mapea un DTO de actualización a un modelo de dominio.

    Args:
        user_dto: DTO con los datos a actualizar

    Returns:
        User: Modelo de dominio de usuario
    """
    return User(
        id=user_dto.id,
        email=user_dto.email,
        password=user_dto.password,
        profile_id=user_dto.profile_id,
        status_id=user_dto.status_id,
    )