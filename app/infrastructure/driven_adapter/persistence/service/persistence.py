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

logger: Final = logging.getLogger("Persistence")

class Persistence(PersistenceGateway):
    """
    Implementación asíncrona del gateway de persistencia que maneja las operaciones de base de datos.
    
    Esta clase implementa la interfaz PersistenceGateway y proporciona métodos para
    realizar operaciones CRUD en la base de datos utilizando SQLAlchemy en modo asíncrono.
    
    Attributes:
        session (AsyncSession): Sesión de SQLAlchemy asíncrona para operaciones de base de datos.
        user_repository (UserRepository): Repositorio para operaciones específicas de usuarios.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """
        Inicializa el servicio de persistencia.
        
        Args:
            session (AsyncSession): Sesión de SQLAlchemy asíncrona para operaciones de base de datos.
        """
        logger.info("Inicializando servicio de persistencia asíncrono")
        self.session: Final[AsyncSession] = session
        self.user_repository: Final[UserRepository] = UserRepository(session)

    async def create_user(self, user: User) -> User:
        """
        Crea un nuevo usuario en la base de datos.
        
        Args:
            user (User): Objeto de dominio User a crear.
            
        Returns:
            User: Usuario creado con su ID asignado.
            
        Raises:
            CustomException: Si hay un error en la validación o en la operación de base de datos.
        """
        try:
            # La validación de email duplicado se delega al repositorio,
            # que capturará la IntegrityError de la base de datos.
            return await self.user_repository.create_user(user)
        except CustomException as e:
            await self.session.rollback()
            raise e
        except (SQLAlchemyError, IntegrityError) as e:
            logger.error(f"Error de base de datos al crear usuario: {e}")
            await self.session.rollback()
            # Mapear a una excepción de dominio genérica de BD
            raise CustomException(ResponseCodeEnum.KOG02)
        
    async def get_user_by_id(self, id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID.
        
        Args:
            id (int): ID del usuario a buscar.
            
        Returns:
            Optional[User]: Usuario encontrado o None si no existe.
            
        Raises:
            CustomException: Si hay un error en la operación de base de datos.
        """
        try:
            return await self.user_repository.get_user_by_id(id)
        except CustomException as e:
            raise e
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener usuario por ID: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
        
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email (str): Email del usuario a buscar.
            
        Returns:
            Optional[User]: Usuario encontrado o None si no existe.
            
        Raises:
            CustomException: Si hay un error en la operación de base de datos.
        """
        try:
            return await self.user_repository.get_user_by_email(email)
        except CustomException as e:
            raise e
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener usuario por email: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
    
    async def update_user(self, user: User) -> User:
        """
        Actualiza un usuario existente en la base de datos.
        
        Args:
            user (User): Objeto de dominio User con los datos actualizados.
            
        Returns:
            User: Usuario actualizado.
            
        Raises:
            CustomException: Si el usuario no existe o hay un error en la operación.
        """
        try:
            # La validación de existencia se delega al repositorio.
            return await self.user_repository.update_user(user)
        except CustomException as e:
            await self.session.rollback()
            raise e
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar usuario: {e}")
            await self.session.rollback()
            raise CustomException(ResponseCodeEnum.KOG02)
