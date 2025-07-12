import logging
from typing import Final, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.infrastructure.driven_adapter.persistence.entity.user_entity import UserEntity


logger: Final[logging.Logger] = logging.getLogger("UserRepository")


class UserRepository:
    """
    Capa de Acceso a Datos (DAL) para la entidad de Usuario.
    
    Esta clase implementa las operaciones CRUD básicas y directas con la base de datos
    para la entidad UserEntity, utilizando SQLAlchemy en modo asíncrono.
    Su responsabilidad es exclusivamente la interacción con la BD, sin lógica de negocio
    ni conocimiento del dominio.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Inicializa el repositorio de usuarios.

        Args:
            session: Sesión de SQLAlchemy asíncrona para operaciones de base de datos.
        """
        self.session: Final[AsyncSession] = session

    async def create_user(self, user_entity: UserEntity) -> UserEntity:
        """
        Crea una nueva entidad de usuario en la base de datos.

        Args:
            user_entity: La entidad de usuario a crear.

        Returns:
            UserEntity: La entidad de usuario creada con su ID asignado.
        
        Raises:
            IntegrityError: Si ocurre una violación de constraints (ej. email duplicado).
            SQLAlchemyError: Para otros errores relacionados con la base de datos.
        """
        logger.info(f"Creando entidad de usuario para el email: {user_entity.email}")
        self.session.add(user_entity)
        await self.session.flush()  # Flush para obtener el ID antes del commit
        await self.session.refresh(user_entity)
        return user_entity

    async def get_user_by_id(self, user_id: int) -> Optional[UserEntity]:
        """
        Obtiene una entidad de usuario por su ID.

        Args:
            user_id: ID de la entidad a buscar.

        Returns:
            Optional[UserEntity]: La entidad encontrada o None si no existe.
        
        Raises:
            SQLAlchemyError: Si ocurre un error en la consulta.
        """
        logger.info(f"Buscando entidad de usuario con ID: {user_id}")
        stmt = select(UserEntity).where(UserEntity.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        """
        Obtiene una entidad de usuario por su email.

        Args:
            email: Email de la entidad a buscar.

        Returns:
            Optional[UserEntity]: La entidad encontrada o None si no existe.
        
        Raises:
            SQLAlchemyError: Si ocurre un error en la consulta.
        """
        logger.info(f"Buscando entidad de usuario con email: {email}")
        stmt = select(UserEntity).where(UserEntity.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update_user(self, user_entity: UserEntity) -> UserEntity:
        """
        Actualiza una entidad de usuario existente. SQLAlchemy se encarga de
        detectar los cambios en la entidad adjunta a la sesión.

        Args:
            user_entity: La entidad de usuario con los datos actualizados.

        Returns:
            UserEntity: La entidad de usuario actualizada.
            
        Raises:
            SQLAlchemyError: Si ocurre un error durante la actualización.
        """
        logger.info(f"Actualizando entidad de usuario con ID: {user_entity.id}")
        self.session.add(user_entity)
        await self.session.flush()
        await self.session.refresh(user_entity)
        return user_entity
