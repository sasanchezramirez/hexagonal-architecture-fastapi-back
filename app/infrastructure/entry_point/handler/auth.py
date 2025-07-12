import logging
from typing import Final

from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from app.infrastructure.entry_point.validator.validator import validate_new_user, validate_get_user, validate_login, validate_update_user
from app.infrastructure.entry_point.mapper.user_mapper import (
    map_user_dto_to_user,
    map_get_user_dto_to_user,
    map_login_dto_to_user,
    map_update_user_dto_to_user,
    map_user_to_user_output_dto
)
from app.infrastructure.entry_point.dto.user_dto import NewUserInput, GetUser, LoginInput, Token, UpdateUserInput
from app.domain.usecase.user_usecase import UserUseCase
from app.domain.usecase.auth_usecase import AuthUseCase
from app.application.container import Container
from app.domain.usecase.util.jwt import get_current_user
from app.domain.model.util.response_codes import ResponseCodeEnum
from app.infrastructure.entry_point.dto.response_dto import ResponseDTO
from app.infrastructure.entry_point.utils.api_response import ApiResponse

logger: Final[logging.Logger] = logging.getLogger("Auth Handler")

router: Final[APIRouter] = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={
        400: {"description": "Validation Error", "model": ResponseDTO},
        401: {"description": "Unauthorized", "model": ResponseDTO},
        500: {"description": "Internal Server Error", "model": ResponseDTO},
    }
)

@router.post('/create-user', response_model=ResponseDTO, status_code=201)
@inject
async def create_user(
    user_dto: NewUserInput,
    user_usecase: UserUseCase = Depends(Provide[Container.user_usecase])
) -> ResponseDTO:
    """
    Crea un nuevo usuario en el sistema.
    """
    logger.info("Iniciando creación de usuario")
    validate_new_user(user_dto)
    user = map_user_dto_to_user(user_dto)
    created_user = await user_usecase.create_user(user)
    response_data = map_user_to_user_output_dto(created_user).model_dump()
    return ApiResponse.create_response(ResponseCodeEnum.KO000, response_data)

@router.post('/get-user', response_model=ResponseDTO)
@inject
async def get_user(
    get_user_dto: GetUser,
    user_usecase: UserUseCase = Depends(Provide[Container.user_usecase]),
    current_user: str = Depends(get_current_user)
) -> ResponseDTO:
    """
    Obtiene los detalles de un usuario.
    """
    logger.info("Iniciando obtención de usuario")
    validate_get_user(get_user_dto)
    user = map_get_user_dto_to_user(get_user_dto)
    found_user = await user_usecase.get_user(user)
    response_data = map_user_to_user_output_dto(found_user).model_dump()
    return ApiResponse.create_response(ResponseCodeEnum.KO000, response_data)

@router.post('/login', response_model=ResponseDTO)
@inject
async def login(
    login_dto: LoginInput,
    auth_usecase: AuthUseCase = Depends(Provide[Container.auth_usecase])
) -> ResponseDTO:
    """
    Autentica un usuario y genera un token de acceso.
    """
    logger.info("Iniciando proceso de login")
    validate_login(login_dto)
    user = map_login_dto_to_user(login_dto)
    token = await auth_usecase.authenticate_user(user)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
        
    token_response = Token(access_token=token, token_type="bearer").model_dump()
    return ApiResponse.create_response(ResponseCodeEnum.KO000, token_response)

@router.post('/update-user', response_model=ResponseDTO)
@inject
async def update_user(
    update_user_dto: UpdateUserInput,
    user_usecase: UserUseCase = Depends(Provide[Container.user_usecase]),
    current_user: str = Depends(get_current_user)
) -> ResponseDTO:
    """
    Actualiza los detalles de un usuario.
    """
    logger.info("Iniciando actualización de usuario")
    validate_update_user(update_user_dto)
    user = map_update_user_dto_to_user(update_user_dto)
    updated_user = await user_usecase.update_user(user)
    response_data = map_user_to_user_output_dto(updated_user).model_dump()
    return ApiResponse.create_response(ResponseCodeEnum.KO000, response_data)
