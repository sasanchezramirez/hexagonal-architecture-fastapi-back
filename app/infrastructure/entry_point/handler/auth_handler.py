import logging
from typing import Final

from app.infrastructure.entry_point.mapper.user_mapper import (
    map_user_dto_to_user,
    map_login_dto_to_user,
    map_update_user_dto_to_user,
    map_user_to_user_output_dto
)
from app.infrastructure.entry_point.dto.user_dto import NewUserInput, GetUser, LoginInput, Token, UpdateUserInput, UserOutput
from app.domain.usecase.user_usecase import UserUseCase
from app.domain.usecase.auth_usecase import AuthUseCase

logger: Final[logging.Logger] = logging.getLogger(__name__)

class AuthHandler:
    """
    Handler for authentication and user management operations.
    Orchestrates validation, mapping, and use case execution.
    """

    def __init__(self, user_usecase: UserUseCase, auth_usecase: AuthUseCase):
        self.user_usecase = user_usecase
        self.auth_usecase = auth_usecase

    async def create_user(self, user_dto: NewUserInput) -> UserOutput:
        logger.info("Starting user creation.")
        user = map_user_dto_to_user(user_dto)
        created_user = await self.user_usecase.create_user(user)
        return map_user_to_user_output_dto(created_user)

    async def get_user(self, get_user_dto: GetUser, current_user_sub: str) -> UserOutput:
        logger.info(f"Starting user retrieval by '{current_user_sub}'.")
        
        found_user = None
        if get_user_dto.email:
            logger.info(f"Searching user by email: {get_user_dto.email}")
            found_user = await self.user_usecase.get_user_by_email(get_user_dto.email)
        elif get_user_dto.id:
            logger.info(f"Searching user by ID: {get_user_dto.id}")
            found_user = await self.user_usecase.get_user_by_id(get_user_dto.id)

        return map_user_to_user_output_dto(found_user)

    async def login(self, login_dto: LoginInput) -> Token:
        logger.info(f"Starting login process for '{login_dto.email}'.")
        user = map_login_dto_to_user(login_dto)
        token_str = await self.auth_usecase.authenticate_user(user)
        return Token(access_token=token_str, token_type="bearer")

    async def update_user(self, update_user_dto: UpdateUserInput, current_user_sub: str) -> UserOutput:
        logger.info(f"Starting user update by '{current_user_sub}'.")
        user = map_update_user_dto_to_user(update_user_dto)
        updated_user = await self.user_usecase.update_user(user)
        return map_user_to_user_output_dto(updated_user)
