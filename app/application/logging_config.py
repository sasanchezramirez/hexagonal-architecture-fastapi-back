import os
import logging
import sys
from typing import Final
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv

load_dotenv()


def configure_logging() -> None:
    """
    Configures the application logging based on the environment.
    
    If ENV (or ENVIRONMENT) is 'local', it uses a standard console formatter.
    Otherwise (e.g., 'production', 'dev'), it uses a JSON formatter for structured logging.
    """
    # Check ENV first (user preference), then ENVIRONMENT, default to 'local'
    environment: Final[str] = os.getenv("ENV", os.getenv("ENVIRONMENT", "local"))
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    
    if environment == "local":
        # Human-readable format for development
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    else:
        # JSON format for production/machines
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        
    handler.setFormatter(formatter)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers = []
    logger.addHandler(handler)
    
    # Set specific levels for noisy libraries if needed
    logging.getLogger("uvicorn.access").handlers = [] # Let root logger handle it or configure separately
