import logging
from typing import Final, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from app.application.settings import settings


logger: Final[logging.Logger] = logging.getLogger("Database Configuration")


def get_database_url() -> str:
    """
    Obtiene la URL de conexión a la base de datos según el entorno.

    Returns:
        str: URL de conexión a la base de datos
    """
    if settings.ENV == 'local':
        return settings.DATABASE_URL
    
    return f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


# Configuración de la base de datos
DATABASE_URL: Final[str] = get_database_url()
logger.info(f"Iniciando conexión a base de datos en entorno {settings.ENV}")

engine: Final = create_engine(DATABASE_URL)
SessionLocal: Final = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: Final = declarative_base()


def get_session() -> Generator[Session, None, None]:
    """
    Genera una sesión de base de datos.

    Yields:
        Session: Sesión de SQLAlchemy

    Note:
        La sesión se cierra automáticamente después de su uso.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
