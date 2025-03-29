from typing import Final

from app.domain.model.user import User
from app.infrastructure.driven_adapter.persistence.entity.user_entity import UserEntity


def map_user_to_entity(user: User) -> UserEntity:
    """
    Mapea un modelo de dominio a una entidad de usuario.

    Args:
        user: Modelo de dominio de usuario

    Returns:
        UserEntity: Entidad de usuario para la base de datos
    """
    return UserEntity.from_user(user)


def map_entity_to_user(user_entity: UserEntity) -> User:
    """
    Mapea una entidad de usuario a un modelo de dominio.

    Args:
        user_entity: Entidad de usuario de la base de datos

    Returns:
        User: Modelo de dominio de usuario
    """
    return User(
        id=user_entity.id,
        email=user_entity.email,
        password=user_entity.password,
        creation_date=str(user_entity.creation_date),
        profile_id=user_entity.profile_id,
        status_id=user_entity.status_id
    )


def map_update_to_entity(user_update: User, user_entity: UserEntity) -> UserEntity:
    """
    Actualiza una entidad de usuario con los datos de un modelo de dominio.

    Args:
        user_update: Modelo de dominio con los datos a actualizar
        user_entity: Entidad de usuario a actualizar

    Returns:
        UserEntity: Entidad de usuario actualizada
    """
    user_entity.id = user_update.id
    if user_update.email:
        user_entity.email = user_update.email
    if user_update.password:
        user_entity.password = user_update.password
    if user_update.profile_id is not None and user_update.profile_id != 0:
        user_entity.profile_id = user_update.profile_id
    if user_update.status_id is not None and user_update.status_id != 0:
        user_entity.status_id = user_update.status_id
    return user_entity

