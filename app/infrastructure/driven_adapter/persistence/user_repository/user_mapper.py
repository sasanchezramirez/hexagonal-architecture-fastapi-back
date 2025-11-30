from app.domain.model.user import User
from app.infrastructure.driven_adapter.persistence.entity.user_entity import UserEntity

class UserMapper:
    @staticmethod
    def to_domain(entity: UserEntity) -> User:
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
        return UserEntity(
            id=domain.id,
            email=domain.email,
            password=domain.password,
            creation_date=domain.creation_date,
            profile_id=domain.profile_id,
            status_id=domain.status_id
        )
