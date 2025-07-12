from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class NewUserInput(BaseModel):
    """
    DTO para la creación de un nuevo usuario.
    """
    email: EmailStr = Field(
        description="Correo electrónico del usuario",
        example="usuario@ejemplo.com"
    )
    password: str = Field(
        description="Contraseña del usuario",
        min_length=8,
        example="contraseña123"
    )
    profile_id: int = Field(
        description="ID del perfil del usuario",
        gt=0,
        example=1
    )
    status_id: int = Field(
        description="ID del estado del usuario",
        gt=0,
        example=1
    )


class UserOutput(BaseModel):
    """
    DTO para la respuesta de datos de usuario.
    """
    id: int = Field(
        description="Identificador único del usuario",
        example=1
    )
    email: EmailStr = Field(
        description="Correo electrónico del usuario",
        example="usuario@ejemplo.com"
    )
    creation_date: str = Field(
        description="Fecha de creación del usuario",
        example="2024-03-27T12:00:00"
    )
    profile_id: int = Field(
        description="ID del perfil del usuario",
        example=1
    )
    status_id: int = Field(
        description="ID del estado del usuario",
        example=1
    )


class GetUser(BaseModel):
    """
    DTO para la búsqueda de un usuario.
    """
    id: Optional[int] = Field(
        default=None,
        description="ID del usuario a buscar",
        example=1
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="Correo electrónico del usuario a buscar",
        example="usuario@ejemplo.com"
    )

    @field_validator('email', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        """Convierte un string vacío a None antes de la validación."""
        if v == "":
            return None
        return v


class Token(BaseModel):
    """
    DTO para la respuesta de autenticación.
    """
    access_token: str = Field(
        description="Token de acceso JWT",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )
    token_type: str = Field(
        description="Tipo de token",
        default="bearer",
        example="bearer"
    )


class LoginInput(BaseModel):
    """
    DTO para el inicio de sesión.
    """
    email: EmailStr = Field(
        description="Correo electrónico del usuario",
        example="usuario@ejemplo.com"
    )
    password: str = Field(
        description="Contraseña del usuario",
        min_length=8,
        example="contraseña123"
    )


class UpdateUserInput(BaseModel):
    """
    DTO para la actualización de un usuario.
    """
    id: int = Field(
        description="ID del usuario a actualizar",
        gt=0,
        example=1
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="Nuevo correo electrónico del usuario",
        example="nuevo@ejemplo.com"
    )
    password: Optional[str] = Field(
        default=None,
        description="Nueva contraseña del usuario. Si está vacío, no se actualizará la contraseña.",
        example="nuevaContraseña123"
    )
    profile_id: Optional[int] = Field(
        default=None,
        description="Nuevo ID del perfil del usuario",
        gt=0,
        example=2
    )
    status_id: Optional[int] = Field(
        default=None,
        description="Nuevo ID del estado del usuario",
        gt=0,
        example=2
    )

    @field_validator('password', mode='before')
    @classmethod
    def validate_password(cls, v):
        """
        Convierte un string vacío a None y valida la longitud
        solo si se proporciona un valor.
        """
        if v == "":
            return None
        if v is not None and len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v
