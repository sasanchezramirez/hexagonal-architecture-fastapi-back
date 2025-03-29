from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from typing import Optional

from app.infrastructure.driven_adapter.persistence.config.database import Base
from app.domain.model.user import User


class UserEntity(Base):
    """
    Entidad de base de datos para usuarios.
    
    Esta clase representa la tabla de usuarios en la base de datos
    utilizando SQLAlchemy como ORM.
    """

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    password: str = Column(String, nullable=False)
    creation_date: str = Column(String, nullable=False)
    profile_id: Optional[int] = Column(Integer, nullable=True)
    status_id: Optional[int] = Column(Integer, nullable=True)

    def __init__(self, email: str, password: str, creation_date: str, 
                 profile_id: Optional[int] = None, status_id: Optional[int] = None) -> None:
        """
        Inicializa una entidad de usuario.

        Args:
            email: Correo electrónico del usuario
            password: Contraseña del usuario
            creation_date: Fecha de creación del usuario
            profile_id: ID del perfil del usuario (opcional)
            status_id: ID del estado del usuario (opcional)
        """
        self.email = email
        self.password = password
        self.creation_date = creation_date
        self.profile_id = profile_id
        self.status_id = status_id

    @classmethod
    def from_user(cls, user: User) -> 'UserEntity':
        """
        Crea una entidad de usuario a partir de un modelo de dominio.

        Args:
            user: Modelo de dominio de usuario

        Returns:
            UserEntity: Entidad de usuario
        """
        return cls(
            email=user.email,
            password=user.password or "",  # Si no hay contraseña, usar cadena vacía
            creation_date=user.creation_date,
            profile_id=user.profile_id,
            status_id=user.status_id
        )

    def __repr__(self) -> str:
        """
        Representación en string de la entidad.

        Returns:
            str: Representación de la entidad
        """
        return f"<UserEntity(id={self.id}, email={self.email})>"


