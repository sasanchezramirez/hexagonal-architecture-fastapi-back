import logging
from typing import Final, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.application.settings import settings


logger: Final[logging.Logger] = logging.getLogger("Database Configuration")


def get_database_url() -> str:
    """
    Gets the database connection URL based on the environment.

    Returns:
        str: Database connection URL
    """
    if settings.DATABASE_URL:
        if 'postgresql' in settings.DATABASE_URL and '+asyncpg' not in settings.DATABASE_URL:
            return settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
        return settings.DATABASE_URL
    
    return f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


DATABASE_URL: Final[str] = get_database_url()
logger.info(f"Starting async database connection in {settings.ENV} environment")

engine: Final = create_async_engine(DATABASE_URL)
AsyncSessionLocal: Final = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
Base: Final = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Generates an asynchronous database session.

    Yields:
        AsyncSession: Asynchronous SQLAlchemy session

    Note:
        The session is automatically closed after use thanks to the `async with` context.
    """
    async with AsyncSessionLocal() as session:
        yield session
