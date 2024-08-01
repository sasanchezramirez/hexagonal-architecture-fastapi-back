from datetime import datetime
from app.domain.model.user import User
from app.infrastructure.entry_point.dto.user_dto import NewUserInput, GetUser, UserOutput

def map_user_dto_to_user(user_dto: NewUserInput) -> User:
        return User(
            email=user_dto.email,
            password=user_dto.password,
            profile_id=user_dto.profile_id,
            status_id=user_dto.status_id,
        )

def map_user_to_user_output_dto(user: User) -> UserOutput:
        return UserOutput(
                id=user.id,
                email=user.email,
                creation_date=user.creation_date,
                profile_id=user.profile_id,
                status_id=user.status_id
        )

def map_get_user_dto_to_user(user_dto: GetUser) -> User:
        return User(
            id = user_dto.id,
            email = user_dto.email
        )