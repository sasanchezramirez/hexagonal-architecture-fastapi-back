from app.domain.model.user import User
from app.infrastructure.driven_adapter.persistence.entity.user_entity import UserEntity

class UserMapper:
    """
    Mapper class to convert between UserEntity and User domain model.
    """
    @staticmethod
    def to_domain(entity: UserEntity) -> User:
        """
        Converts a UserEntity to a User domain model.
        
        Args:
            entity: The user entity to convert.
            
        Returns:
            User: The converted user domain model.
        """
        if not entity:
            return None
        return User(
            id=entity.id,
            email=entity.email,
            password=entity.password,
            creation_date=entity.creation_date,
            profile_id=entity.profile_id,
            status_id=entity.status_id
        )

    @staticmethod
    def to_entity(domain: User) -> UserEntity:
        """
        Converts a User domain model to a UserEntity.
        
        Args:
            domain: The user domain model to convert.
            
        Returns:
            UserEntity: The converted user entity.
        """
        return UserEntity(
            id=domain.id,
            email=domain.email,
            password=domain.password,
            creation_date=domain.creation_date,
            profile_id=domain.profile_id,
            status_id=domain.status_id
        )
