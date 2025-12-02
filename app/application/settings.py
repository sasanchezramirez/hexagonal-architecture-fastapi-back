from typing import Final, Optional

from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """
    Application configuration.
    
    This class handles loading and validation of all environment
    variables required for the application.
    """
    
    # Execution environment
    ENV: str = Field(
        default="local",
        env="ENV",
        description="Execution environment (local, development, production)"
    )
    
    # Database configuration
    DATABASE_URL: Optional[str] = Field(
        default=None,
        env="DATABASE_URL",
        description="Database connection URL for local environment"
    )
    DB_USER: str = Field(
        default="postgres",
        env="DB_USER",
        description="Database user"
    )
    DB_PASSWORD: str = Field(
        default="postgres",
        env="DB_PASSWORD",
        description="Database password"
    )
    DB_HOST: str = Field(
        default="localhost",
        env="DB_HOST",
        description="Database host"
    )
    DB_PORT: str = Field(
        default="5432",
        env="DB_PORT",
        description="Database port"
    )
    DB_NAME: str = Field(
        default="hexagonal_db",
        env="DB_NAME",
        description="Database name"
    )
    
    # JWT configuration
    SECRET_KEY: str = Field(
        default="your-secret-key",
        env="SECRET_KEY",
        description="Secret key for signing JWT tokens"
    )
    ALGORITHM: str = Field(
        default="HS256",
        env="ALGORITHM",
        description="Encryption algorithm for JWT tokens"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES",
        description="JWT token expiration time in minutes"
    )

    class Config:
        """
        Pydantic configuration.
        """
        env_file = ".env"
        case_sensitive = True


# Global configuration instance
settings: Final[Settings] = Settings()
