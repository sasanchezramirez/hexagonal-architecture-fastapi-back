import logging
from typing import Final, Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.infrastructure.driven_adapter.persistence.mapper.user_mapper import map_user_to_entity, map_entity_to_user
from app.infrastructure.driven_adapter.persistence.entity.user_entity import UserEntity
from app.domain.model.user import User
from app.domain.model.util.response_codes import ResponseCodeEnum
from app.domain.model.util.custom_exceptions import CustomException


logger: Final[logging.Logger] = logging.getLogger("User Repository")


class UserRepository:
    """
    Implementación del repositorio de usuarios.
    
    Esta clase implementa las operaciones de persistencia para usuarios
    utilizando SQLAlchemy como ORM.
    """

    def __init__(self, session: Session) -> None:
        """
        Inicializa el repositorio de usuarios.

        Args:
            session: Sesión de SQLAlchemy para operaciones de base de datos
        """
        self.session: Final[Session] = session

    def create_user(self, user: User) -> User:
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            user: Usuario a crear

        Returns:
            User: Usuario creado con ID asignado

        Raises:
            CustomException: Si hay un error al crear el usuario
        """
        logger.info(f"Creando usuario: {user.email}")
        try:
            user_entity = map_user_to_entity(user)
            self.session.add(user_entity)
            self.session.commit()
            return map_entity_to_user(user_entity)
        except IntegrityError as e:
            logger.error(f"Error de integridad: {e}")
            if "llave duplicada" in str(e.orig) or "duplicate key" in str(e.orig):
                raise CustomException(ResponseCodeEnum.KOU01)
            elif "viola la llave" in str(e.orig) or "key violation" in str(e.orig):
                if "profile_id" in str(e.orig):
                    raise CustomException(ResponseCodeEnum.KOU03)
                elif "status_id" in str(e.orig):
                    raise CustomException(ResponseCodeEnum.KOU04)
            raise CustomException(ResponseCodeEnum.KOG02)
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
        except Exception as e:
            logger.error(f"Error no manejado: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)

    def get_user_by_id(self, id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID.

        Args:
            id: ID del usuario a buscar

        Returns:
            Optional[User]: Usuario encontrado o None si no existe

        Raises:
            CustomException: Si hay un error al obtener el usuario
        """
        try:
            user_entity = self.session.query(UserEntity).filter(UserEntity.id == id).first()
            if not user_entity:
                logger.error(f"Usuario con ID {id} no encontrado")
                raise CustomException(ResponseCodeEnum.KOU02)
            return map_entity_to_user(user_entity)
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
        except Exception as e:
            logger.error(f"Error no manejado: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su email.

        Args:
            email: Email del usuario a buscar

        Returns:
            Optional[User]: Usuario encontrado o None si no existe

        Raises:
            CustomException: Si hay un error al obtener el usuario
        """
        try:
            logger.info(f"Buscando usuario con email: {email}")
            user_entity = self.session.query(UserEntity).filter(UserEntity.email == email).first()
            if not user_entity:
                logger.info(f"Usuario con email {email} no encontrado")
                return None
            return map_entity_to_user(user_entity)
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
        except Exception as e:
            logger.error(f"Error no manejado: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)

    def update_user(self, user: User) -> User:
        """
        Actualiza un usuario existente.

        Args:
            user: Usuario a actualizar

        Returns:
            User: Usuario actualizado

        Raises:
            CustomException: Si hay un error al actualizar el usuario
        """
        try:
            user_entity = self.session.query(UserEntity).filter(UserEntity.id == user.id).first()
            if not user_entity:
                logger.error(f"Usuario con ID {user.id} no encontrado")
                raise CustomException(ResponseCodeEnum.KOU02)
            
            updated_entity = map_user_to_entity(user)
            for key, value in updated_entity.__dict__.items():
                if key != '_sa_instance_state' and value is not None:
                    setattr(user_entity, key, value)
            
            self.session.commit()
            return map_entity_to_user(user_entity)
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
        except Exception as e:
            logger.error(f"Error no manejado: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)
