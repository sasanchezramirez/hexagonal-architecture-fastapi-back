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

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: ID del usuario a buscar

        Returns:
            Optional[User]: Usuario encontrado o None si no existe

        Raises:
            CustomException: Si hay un error al obtener el usuario
        """
        logger.info(f"Buscando usuario con ID: {user_id}")
        try:
            user_entity = self.session.query(UserEntity).filter_by(id=user_id).first()
            if user_entity is None:
                logger.error(f"Usuario con ID {user_id} no encontrado")
                raise CustomException(ResponseCodeEnum.KOU02)
            return map_entity_to_user(user_entity)
        except CustomException as e:
            raise
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
        except Exception as e:
            logger.error(f"Error no manejado: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su correo electrónico.

        Args:
            email: Correo electrónico del usuario a buscar

        Returns:
            Optional[User]: Usuario encontrado o None si no existe

        Raises:
            CustomException: Si hay un error al obtener el usuario
        """
        logger.info(f"Buscando usuario con email: {email}")
        try:
            user_entity = self.session.query(UserEntity).filter_by(email=email).first()
            if user_entity is None:
                logger.error(f"Usuario con email {email} no encontrado")
                raise CustomException(ResponseCodeEnum.KOU02)
            return map_entity_to_user(user_entity)
        except CustomException as e:
            raise
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos: {e}")
            raise CustomException(ResponseCodeEnum.KOG02)
        except Exception as e:
            logger.error(f"Error no manejado: {e}")
            raise CustomException(ResponseCodeEnum.KOG01)

    def update_user(self, user: User) -> User:
        """
        Actualiza los datos de un usuario existente.

        Args:
            user: Usuario con los datos a actualizar

        Returns:
            User: Usuario actualizado

        Raises:
            CustomException: Si hay un error al actualizar el usuario
        """
        logger.info(f"Actualizando usuario: {user.email}")
        try:
            existing_user = self.session.query(UserEntity).filter_by(id=user.id).first()
            if not existing_user:
                raise CustomException(ResponseCodeEnum.KOD02)

            if user.email:
                existing_user.email = user.email
            if user.password:
                existing_user.password = user.password
            if user.profile_id is not None and user.profile_id != 0:
                existing_user.profile_id = user.profile_id
            if user.status_id is not None and user.status_id != 0:
                existing_user.status_id = user.status_id

            self.session.commit()
            return map_entity_to_user(existing_user)
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
