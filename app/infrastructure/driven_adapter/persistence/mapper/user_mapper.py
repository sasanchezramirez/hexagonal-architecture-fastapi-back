from app.infrastructure.driven_adapter.persistence.entity.user_entity import User_entity
from app.domain.model.user import User


def map_user_entity_to_user(user_entity: User_entity) -> User:
    return User(
        id=user_entity.id,
        email=user_entity.email,
        password=user_entity.password,
        creation_date=str(user_entity.creation_date),
        profile_id=user_entity.profile_id,
        status_id=user_entity.status_id
    )