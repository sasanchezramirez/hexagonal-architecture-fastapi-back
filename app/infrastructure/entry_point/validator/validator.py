from typing import Final
import re

from pydantic import ValidationError, EmailStr
from app.infrastructure.entry_point.dto.user_dto import (
    NewUserInput,
    GetUser,
    LoginInput,
    UpdateUserInput
)


def is_valid_email(email: str) -> bool:
    """
    Valida el formato de un correo electrónico de manera más flexible.
    
    Args:
        email: Correo electrónico a validar
        
    Returns:
        bool: True si el formato es válido
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_new_user(user: NewUserInput) -> bool:
    """
    Valida los datos de un nuevo usuario.

    Args:
        user: DTO con los datos del nuevo usuario

    Returns:
        bool: True si la validación es exitosa

    Raises:
        ValueError: Si los datos no son válidos
    """
    if not user.email:
        raise ValueError("El correo electrónico es obligatorio")
    
    if not is_valid_email(user.email):
        raise ValueError("El formato del correo electrónico no es válido")
    
    if not user.password or len(user.password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    
    if not user.profile_id or user.profile_id <= 0:
        raise ValueError("El ID del perfil debe ser mayor que 0")
    
    if not user.status_id or user.status_id <= 0:
        raise ValueError("El ID del estado debe ser mayor que 0")
    
    return True


def validate_get_user(user: GetUser) -> bool:
    """
    Valida los criterios de búsqueda de usuario.

    Args:
        user: DTO con los criterios de búsqueda

    Returns:
        bool: True si la validación es exitosa

    Raises:
        ValueError: Si los datos no son válidos
    """
    if not user.id and not user.email:
        raise ValueError("Debe proporcionar un ID o correo electrónico")
    
    if user.email and not is_valid_email(user.email):
        raise ValueError("El formato del correo electrónico no es válido")
    
    return True


def validate_login(user: LoginInput) -> bool:
    """
    Valida las credenciales de inicio de sesión.

    Args:
        user: DTO con las credenciales de login

    Returns:
        bool: True si la validación es exitosa

    Raises:
        ValueError: Si los datos no son válidos
    """
    if not user.email:
        raise ValueError("El correo electrónico es obligatorio")
    
    if not is_valid_email(user.email):
        raise ValueError("El formato del correo electrónico no es válido")
    
    if not user.password or len(user.password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    
    return True


def validate_update_user(user: UpdateUserInput) -> bool:
    """
    Valida los datos de actualización de usuario.

    Args:
        user: DTO con los datos a actualizar

    Returns:
        bool: True si la validación es exitosa

    Raises:
        ValueError: Si los datos no son válidos
    """
    if not user.id or user.id <= 0:
        raise ValueError("El ID del usuario es obligatorio y debe ser mayor que 0")
    
    if user.email and not is_valid_email(user.email):
        raise ValueError("El formato del correo electrónico no es válido")
    
    if user.password and len(user.password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    
    if user.profile_id is not None and user.profile_id <= 0:
        raise ValueError("El ID del perfil debe ser mayor que 0")
    
    if user.status_id is not None and user.status_id <= 0:
        raise ValueError("El ID del estado debe ser mayor que 0")
    
    return True
