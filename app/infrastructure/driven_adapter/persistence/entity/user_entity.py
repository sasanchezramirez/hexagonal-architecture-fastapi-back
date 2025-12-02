from sqlalchemy import Column, Integer, String
from typing import Optional

from app.infrastructure.driven_adapter.persistence.config.database import Base



class UserEntity(Base):
    """
    Database entity for users.
    
    This class represents the users table in the database
    using SQLAlchemy as ORM.
    """

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    password: str = Column(String, nullable=False)
    creation_date: str = Column(String, nullable=False)
    profile_id: Optional[int] = Column(Integer, nullable=True)
    status_id: Optional[int] = Column(Integer, nullable=True)

    def __init__(self, email: str, password: str, creation_date: str, 
                 id: Optional[int] = None, profile_id: Optional[int] = None, status_id: Optional[int] = None) -> None:
        """
        Initializes a user entity.

        Args:
            email: User's email
            password: User's password
            creation_date: User's creation date
            profile_id: User's profile ID (optional)
            status_id: User's status ID (optional)
        """
        self.id = id
        self.email = email
        self.password = password
        self.creation_date = creation_date
        self.profile_id = profile_id
        self.status_id = status_id



    def __repr__(self) -> str:
        """
        String representation of the entity.

        Returns:
            str: Entity representation
        """
        return f"<UserEntity(id={self.id}, email={self.email})>"


