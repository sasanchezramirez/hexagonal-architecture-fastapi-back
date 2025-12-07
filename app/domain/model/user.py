from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    """
    Domain model representing a user in the system.
    
    This model defines the data structure and validations
    required for a user in the system.
    """
    
    id: Optional[int] = Field(
        default=None,
        description="Unique identifier of the user"
    )
    
    email: EmailStr = Field(
        description="User's email address",
        example="user@example.com"
    )
    
    password: Optional[str] = Field(
        default=None,
        description="User's hashed password",
        min_length=8
    )
    
    creation_date: str = Field(
        description="User creation date in ISO format"
    )
    
    profile_id: Optional[int] = Field(
        default=None,
        description="User's profile identifier",
        gt=0
    )
    
    status_id: Optional[int] = Field(
        default=None,
        description="User's status identifier",
        gt=0
    )

    class Config:
        """
        Pydantic model configuration.
        """
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "creation_date": "2024-03-27T12:00:00",
                "profile_id": 1,
                "status_id": 1
            }
        }
