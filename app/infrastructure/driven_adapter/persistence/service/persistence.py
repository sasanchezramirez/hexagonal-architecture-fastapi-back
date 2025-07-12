import logging
from typing import Optional, Final

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.infrastructure.driven_adapter.persistence.repository.user_repository import UserRepository
from app.domain.model.user import User
from app.domain.gateway.persistence_gateway import PersistenceGateway
from app.domain.model.util.custom_exceptions import CustomException
from app.domain.model.util.response_codes import ResponseCodeEnum
import app.infrastructure.driven_adapter.persistence.mapper.user_mapper as mapper

logger: Final = logging.getLogger("PersistenceAdapter")

class Persistence(PersistenceGateway):
    """
    Implementación del Gateway de Persistencia (Adaptador).
    
    Esta clase implementa la interfaz `PersistenceGateway` y actúa como
    un adaptador que traduce las necesidades del dominio en operaciones
    de base de datos, orquestando el repositorio y los mappers.
    
    Responsabilidades:
    - Mapear modelos de dominio a entidades de BD y viceversa.
    - Orquestar operaciones en el repositorio.
    - Manejar transacciones (commit/rollback).
    - Traducir errores de la BD a excepciones de dominio.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Inicializa el servicio de persistencia.
        """
        logger.info("Inicializando adaptador de persistencia")
        self.session: Final[AsyncSession] = session
        self.user_repository: Final[UserRepository] = UserRepository(session)

    async def create_user(self, user: User) -> User:
        """
        Orquesta la creación de un nuevo usuario.
        """
        try:
            user_entity = mapper.map_user_to_entity(user)
            created_entity = await self.user_repository.create_user(user_entity)
            await self.session.commit()
            logger.info(f"Usuario creado exitosamente con ID: {created_entity.id}")
            return mapper.map_entity_to_user(created_entity)
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Error de integridad al crear usuario: {e.orig}")
            if "users_email_key" in str(e.orig):
                raise CustomException(ResponseCodeEnum.KOU01)
            raise CustomException(ResponseCodeEnum.KOG02)
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error de SQLAlchemy al crear usuario: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
        
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Orquesta la obtención de un usuario por su ID.
        """
        try:
            user_entity = await self.user_repository.get_user_by_id(user_id)
            if not user_entity:
                return None
            return mapper.map_entity_to_user(user_entity)
        except SQLAlchemyError as e:
            logger.error(f"Error de SQLAlchemy al obtener usuario por ID: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
        
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Orquesta la obtención de un usuario por su email.
        """
        try:
            user_entity = await self.user_repository.get_user_by_email(email)
            if not user_entity:
                return None
            return mapper.map_entity_to_user(user_entity)
        except SQLAlchemyError as e:
            logger.error(f"Error de SQLAlchemy al obtener usuario por email: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
    
    async def update_user(self, user: User) -> User:
        """
        Orquesta la actualización de un usuario existente.
        """
        try:
            # 1. Obtener la entidad existente
            user_entity = await self.user_repository.get_user_by_id(user.id)
            if not user_entity:
                raise CustomException(ResponseCodeEnum.KOU02)
            
            # 2. Actualizar la entidad con los nuevos datos del modelo
            updated_entity = mapper.map_update_to_entity(user, user_entity)

            # 3. Persistir la entidad actualizada
            persisted_entity = await self.user_repository.update_user(updated_entity)
            await self.session.commit()
            logger.info(f"Usuario con ID {persisted_entity.id} actualizado exitosamente.")
            return mapper.map_entity_to_user(persisted_entity)
        except CustomException as e:
            await self.session.rollback()
            raise e
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error(f"Error de SQLAlchemy al actualizar usuario: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
