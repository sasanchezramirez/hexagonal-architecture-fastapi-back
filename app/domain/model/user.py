from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """
    Modelo de dominio para representar un usuario en el sistema.
    
    Este modelo define la estructura de datos y las validaciones
    necesarias para un usuario en el sistema.
    """
    
    id: Optional[int] = Field(
        default=None,
        description="Identificador único del usuario"
    )
    
    email: EmailStr = Field(
        description="Correo electrónico del usuario",
        example="usuario@ejemplo.com"
    )
    
    password: Optional[str] = Field(
        default=None,
        description="Contraseña hasheada del usuario",
        min_length=8
    )
    
    creation_date: str = Field(
        description="Fecha de creación del usuario en formato ISO"
    )
    
    profile_id: Optional[int] = Field(
        default=None,
        description="Identificador del perfil del usuario",
        gt=0
    )
    
    status_id: Optional[int] = Field(
        default=None,
        description="Identificador del estado del usuario",
        gt=0
    )

    class Config:
        """
        Configuración del modelo Pydantic.
        """
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "usuario@ejemplo.com",
                "creation_date": "2024-03-27T12:00:00",
                "profile_id": 1,
                "status_id": 1
            }
        }
