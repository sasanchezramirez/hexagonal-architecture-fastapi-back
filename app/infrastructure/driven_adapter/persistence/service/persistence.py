import logging
from typing import Optional, Final

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.infrastructure.driven_adapter.persistence.entity.user_entity import UserEntity
from app.infrastructure.driven_adapter.persistence.repository.user_repository import UserRepository
from app.domain.model.user import User
from app.domain.gateway.persistence_gateway import PersistenceGateway
from app.domain.model.util.custom_exceptions import CustomException
from app.domain.model.util.response_codes import ResponseCodeEnum
import app.infrastructure.driven_adapter.persistence.mapper.user_mapper as mapper

logger: Final = logging.getLogger("Persistence")

class Persistence(PersistenceGateway):
    """
    Implementación del gateway de persistencia que maneja las operaciones de base de datos.
    
    Esta clase implementa la interfaz PersistenceGateway y proporciona métodos para
    realizar operaciones CRUD en la base de datos utilizando SQLAlchemy.
    
    Attributes:
        session (Session): Sesión de SQLAlchemy para operaciones de base de datos.
        user_repository (UserRepository): Repositorio para operaciones específicas de usuarios.
    """
    
    def __init__(self, session: Session) -> None:
        """
        Inicializa el servicio de persistencia.
        
        Args:
            session (Session): Sesión de SQLAlchemy para operaciones de base de datos.
        """
        logger.info("Inicializando servicio de persistencia")
        self.session: Final[Session] = session
        self.user_repository: Final[UserRepository] = UserRepository(session)

    def create_user(self, user: User) -> User:
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
            # Verificar si el email ya existe
            existing_user = self.user_repository.get_user_by_email(user.email)
            if existing_user:
                raise CustomException(ResponseCodeEnum.KOU01)
                
            user_entity = UserEntity.from_user(user)
            created_user_entity = self.user_repository.create_user(user_entity)
            self.session.commit()
            return mapper.map_entity_to_user(created_user_entity)
        except CustomException as e:
            self.session.rollback()
            raise e
        except IntegrityError as e:
            logger.error(f"Error de integridad al crear usuario: {e}")
            self.session.rollback()
            raise CustomException(ResponseCodeEnum.KOU01)
        except SQLAlchemyError as e:
            logger.error(f"Error al crear usuario: {e}")
            self.session.rollback()
            raise CustomException(ResponseCodeEnum.KOG02)
        
    def get_user_by_id(self, id: int) -> Optional[User]:
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
            user_entity = self.user_repository.get_user_by_id(id)
            return mapper.map_entity_to_user(user_entity)
        except CustomException as e:
            raise e
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener usuario: {e}")
            self.session.rollback()
            raise CustomException(ResponseCodeEnum.KOG02)
        
    def get_user_by_email(self, email: str) -> Optional[User]:
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
            user_entity = self.user_repository.get_user_by_email(email)
            return mapper.map_entity_to_user(user_entity)
        except CustomException as e:
            raise e
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener usuario: {e}")
            self.session.rollback()
            raise CustomException(ResponseCodeEnum.KOG02)
    
    def update_user(self, user: User) -> User:
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
            existing_user = self.user_repository.get_user_by_id(user.id)
            if not existing_user:
                raise CustomException(ResponseCodeEnum.KOU02)
            user_entity = mapper.map_update_to_entity(user, existing_user)
            updated_user_entity = self.user_repository.update_user(user_entity)
            self.session.commit()
            return mapper.map_entity_to_user(updated_user_entity)
        except CustomException as e:
            self.session.rollback()
            raise e
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar usuario: {e}")
            self.session.rollback()
            raise CustomException(ResponseCodeEnum.KOG02)
