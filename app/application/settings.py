from typing import Final, Optional

from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


# Cargar variables de entorno
load_dotenv()


class Settings(BaseSettings):
    """
    Configuración de la aplicación.
    
    Esta clase maneja la carga y validación de todas las variables
    de entorno necesarias para la aplicación.
    """
    
    # Entorno de ejecución
    ENV: str = Field(
        default="local",
        env="ENV",
        description="Entorno de ejecución (local, development, production)"
    )
    
    # Configuración de base de datos
    DATABASE_URL: Optional[str] = Field(
        default=None,
        env="DATABASE_URL",
        description="URL de conexión a la base de datos para entorno local"
    )
    DB_USER: str = Field(
        default="postgres",
        env="DB_USER",
        description="Usuario de la base de datos"
    )
    DB_PASSWORD: str = Field(
        default="postgres",
        env="DB_PASSWORD",
        description="Contraseña de la base de datos"
    )
    DB_HOST: str = Field(
        default="localhost",
        env="DB_HOST",
        description="Host de la base de datos"
    )
    DB_PORT: str = Field(
        default="5432",
        env="DB_PORT",
        description="Puerto de la base de datos"
    )
    DB_NAME: str = Field(
        default="hexagonal_db",
        env="DB_NAME",
        description="Nombre de la base de datos"
    )
    
    # Configuración de JWT
    SECRET_KEY: str = Field(
        default="your-secret-key",
        env="SECRET_KEY",
        description="Clave secreta para firmar tokens JWT"
    )
    ALGORITHM: str = Field(
        default="HS256",
        env="ALGORITHM",
        description="Algoritmo de encriptación para tokens JWT"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES",
        description="Tiempo de expiración de tokens JWT en minutos"
    )

    class Config:
        """
        Configuración de Pydantic.
        """
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings: Final[Settings] = Settings()
