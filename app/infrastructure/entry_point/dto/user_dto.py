from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class NewUserInput(BaseModel):
    """
    DTO for creating a new user.
    """
    email: EmailStr = Field(
        description="User's email address",
        example="user@example.com"
    )
    password: str = Field(
        description="User's password",
        min_length=8,
        example="password123"
    )
    profile_id: int = Field(
        description="User's profile ID",
        gt=0,
        example=1
    )
    status_id: int = Field(
        description="User's status ID",
        gt=0,
        example=1
    )


class UserOutput(BaseModel):
    """
    DTO for user data response.
    """
    id: int = Field(
        description="Unique identifier of the user",
        example=1
    )
    email: EmailStr = Field(
        description="User's email address",
        example="user@example.com"
    )
    creation_date: str = Field(
        description="User creation date",
        example="2024-03-27T12:00:00"
    )
    profile_id: int = Field(
        description="User's profile ID",
        example=1
    )
    status_id: int = Field(
        description="User's status ID",
        example=1
    )


class GetUser(BaseModel):
    """
    DTO for searching a user.
    """
    id: Optional[int] = Field(
        default=None,
        description="ID of the user to search",
        example=1
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="Email of the user to search",
        example="user@example.com"
    )

    @field_validator('email', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        """Converts an empty string to None before validation."""
        if v == "":
            return None
        return v


class Token(BaseModel):
    """
    DTO for authentication response.
    """
    access_token: str = Field(
        description="JWT access token",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )
    token_type: str = Field(
        description="Token type",
        default="bearer",
        example="bearer"
    )


class LoginInput(BaseModel):
    """
    DTO for login.
    """
    email: EmailStr = Field(
        description="User's email address",
        example="user@example.com"
    )
    password: str = Field(
        description="User's password",
        min_length=8,
        example="password123"
    )


class UpdateUserInput(BaseModel):
    """
    DTO for updating a user.
    """
    id: int = Field(
        description="ID of the user to update",
        gt=0,
        example=1
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="New email address of the user",
        example="new@example.com"
    )
    password: Optional[str] = Field(
        default=None,
        description="New password of the user. If empty, password will not be updated.",
        example="newPassword123"
    )
    profile_id: Optional[int] = Field(
        default=None,
        description="New profile ID of the user",
        gt=0,
        example=2
    )
    status_id: Optional[int] = Field(
        default=None,
        description="New status ID of the user",
        gt=0,
        example=2
    )

    @field_validator('password', mode='before')
    @classmethod
    def validate_password(cls, v):
        """
        Converts an empty string to None and validates length
        only if a value is provided.
        """
        if v == "":
            return None
        if v is not None and len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v
