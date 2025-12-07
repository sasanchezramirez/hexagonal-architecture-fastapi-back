from pydantic import BaseModel
from typing import Any, Optional

class ResponseDTO(BaseModel):
    """
    Standard response DTO for API responses.
    """
    apiCode: str
    data: Optional[Any] = None
    message: Optional[str] = None
    status: Optional[bool] = None
