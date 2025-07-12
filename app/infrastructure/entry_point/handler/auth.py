import logging
from typing import Final

from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from app.infrastructure.entry_point.validator.validator import validate_new_user, validate_get_user, validate_login, validate_update_user
from app.infrastructure.entry_point.mapper.user_mapper import (
    map_user_dto_to_user,
    map_get_user_dto_to_user,
    map_login_dto_to_user,
    map_update_user_dto_to_user,
    map_user_to_user_output_dto
)
from app.infrastructure.entry_point.dto.user_dto import NewUserInput, GetUser, LoginInput, Token, UpdateUserInput, UserOutput
from app.domain.usecase.user_usecase import UserUseCase
from app.domain.usecase.auth_usecase import AuthUseCase
from app.application.container import Container
from app.domain.usecase.util.jwt import get_current_user

logger: Final[logging.Logger] = logging.getLogger("AuthHandler")

router: Final[APIRouter] = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/create-user', response_model=UserOutput, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user_dto: NewUserInput,
    user_usecase: UserUseCase = Depends(Provide[Container.user_usecase])
) -> UserOutput:
    """
    Crea un nuevo usuario en el sistema.
    """
    logger.info("Endpoint: Inicia la creación de usuario.")
    validate_new_user(user_dto)
    user = map_user_dto_to_user(user_dto)
    created_user = await user_usecase.create_user(user)
    return map_user_to_user_output_dto(created_user)

@router.post('/get-user', response_model=UserOutput)
@inject
async def get_user(
    get_user_dto: GetUser,
    user_usecase: UserUseCase = Depends(Provide[Container.user_usecase]),
    current_user: dict = Depends(get_current_user)
) -> UserOutput:
    """
    Obtiene los detalles de un usuario por ID o por Email.
    """
    logger.info(f"Endpoint: Inicia la obtención de usuario por '{current_user.get('sub')}'.")
    validate_get_user(get_user_dto)
    
    found_user = None
    if get_user_dto.email:
        logger.info(f"Buscando usuario por email: {get_user_dto.email}")
        found_user = await user_usecase.get_user_by_email(get_user_dto.email)
    elif get_user_dto.id:
        logger.info(f"Buscando usuario por ID: {get_user_dto.id}")
        found_user = await user_usecase.get_user_by_id(get_user_dto.id)

    return map_user_to_user_output_dto(found_user)

@router.post('/login', response_model=Token)
@inject
async def login(
    login_dto: LoginInput,
    auth_usecase: AuthUseCase = Depends(Provide[Container.auth_usecase])
) -> Token:
    """
    Autentica un usuario y genera un token de acceso.
    """
    logger.info(f"Endpoint: Inicia el proceso de login para '{login_dto.email}'.")
    validate_login(login_dto)
    user = map_login_dto_to_user(login_dto)
    token_str = await auth_usecase.authenticate_user(user)
    return Token(access_token=token_str, token_type="bearer")

@router.post('/update-user', response_model=UserOutput)
@inject
async def update_user(
    update_user_dto: UpdateUserInput,
    user_usecase: UserUseCase = Depends(Provide[Container.user_usecase]),
    current_user: dict = Depends(get_current_user)
) -> UserOutput:
    """
    Actualiza los detalles de un usuario.
    """
    logger.info(f"Endpoint: Inicia la actualización de usuario por '{current_user.get('sub')}'.")
    validate_update_user(update_user_dto)
    user = map_update_user_dto_to_user(update_user_dto)
    updated_user = await user_usecase.update_user(user)
    return map_user_to_user_output_dto(updated_user)
