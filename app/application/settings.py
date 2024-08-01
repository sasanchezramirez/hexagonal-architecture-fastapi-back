from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    ENV: str = Field("local", env="ENV")

    DATABASE_URL: Optional[str] = Field(None, env="DATABASE_URL")

    class Config:
        env_file = ".env"

settings = Settings()
