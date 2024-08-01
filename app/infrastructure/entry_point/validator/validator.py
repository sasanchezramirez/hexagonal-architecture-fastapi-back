from pydantic import ValidationError
from app.infrastructure.entry_point.dto.user_dto import NewUserInput, GetUser

def validate_new_user(user: NewUserInput):
    if not user.email or '@' not in user.email:
        raise ValueError("Email is invalid")
    return True

def validate_get_user(user: GetUser):
    if not user.email:
        return True
    elif '@' not in user.email:
        raise ValueError("Email is invalid")
    return True
