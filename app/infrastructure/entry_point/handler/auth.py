import logging
from typing import Final

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
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
from app.domain.model.util.custom_exceptions import CustomException
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
        500: {"description": "Internal Server Error", "model": ResponseDTO},
    }
)

@router.post('/create-user', response_model=ResponseDTO)
@inject
def create_user(
    user_dto: NewUserInput,
    user_usecase: UserUseCase = Depends(Provide[Container.user_usecase])
) -> JSONResponse:
    """
    Crea un nuevo usuario en el sistema.
    
    Args:
        user_dto: Objeto con los datos del usuario
        user_usecase: Caso de uso para operaciones de usuario

    Returns:
        JSONResponse: Respuesta con el resultado de la operación
    """
    logger.info("Iniciando creación de usuario")
    try:
        validate_new_user(user_dto)
        user = map_user_dto_to_user(user_dto)
        user = user_usecase.create_user(user)
        response_data = map_user_to_user_output_dto(user).model_dump()
        return JSONResponse(
            status_code=200,
            content=ApiResponse.create_response(ResponseCodeEnum.KO000, response_data)
        )
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content=ApiResponse.create_response(ResponseCodeEnum.KOD01, str(e))
        )
    except CustomException as e:
        return JSONResponse(
            status_code=e.http_status,
            content=e.to_dict()
        )
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        return JSONResponse(
            status_code=500,
            content=ApiResponse.create_response(ResponseCodeEnum.KOG01)
        )

@router.post('/get-user', response_model=ResponseDTO)
@inject
def get_user(
    get_user_dto: GetUser,
    user_usecase: UserUseCase = Depends(Provide[Container.user_usecase]),
    current_user: str = Depends(get_current_user)
) -> JSONResponse:
    """
    Obtiene los detalles de un usuario.

    Args:
        get_user_dto: Objeto con los datos necesarios para obtener el usuario
        user_usecase: Caso de uso para operaciones de usuario
        current_user: Usuario actual autenticado

    Returns:
        JSONResponse: Respuesta con los datos del usuario
    """
    logger.info("Iniciando obtención de usuario")
    try:
        validate_get_user(get_user_dto)
        user = map_get_user_dto_to_user(get_user_dto)
        user = user_usecase.get_user(user)
        response_data = map_user_to_user_output_dto(user).model_dump()
        return JSONResponse(
            status_code=200,
            content=ApiResponse.create_response(ResponseCodeEnum.KO000, response_data)
        )
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content=ApiResponse.create_response(ResponseCodeEnum.KOD01, str(e))
        )
    except CustomException as e:
        return JSONResponse(
            status_code=e.http_status,
            content=e.to_dict()
        )
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        return JSONResponse(
            status_code=500,
            content=ApiResponse.create_response(ResponseCodeEnum.KOG01)
        )

@router.post('/login', response_model=ResponseDTO)
@inject
def login(
    login_dto: LoginInput,
    auth_usecase: AuthUseCase = Depends(Provide[Container.auth_usecase])
) -> JSONResponse:
    """
    Autentica un usuario y genera un token de acceso.
    
    Args:
        login_dto: Objeto con las credenciales del usuario
        auth_usecase: Caso de uso para operaciones de autenticación

    Returns:
        JSONResponse: Respuesta con el token de acceso
    """
    logger.info("Iniciando proceso de login")
    try:
        validate_login(login_dto)
        user = map_login_dto_to_user(login_dto)
        token = auth_usecase.authenticate_user(user)
        
        if token:
            token_response = Token(access_token=token, token_type="bearer").model_dump()
            return JSONResponse(
                status_code=200,
                content=ApiResponse.create_response(ResponseCodeEnum.KO000, token_response)
            )
        return JSONResponse(
            status_code=401,
            content=ApiResponse.create_response(ResponseCodeEnum.KOD02)
        )
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content=ApiResponse.create_response(ResponseCodeEnum.KOD01, str(e))
        )
    except CustomException as e:
        return JSONResponse(
            status_code=e.http_status,
            content=e.to_dict()
        )
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        return JSONResponse(
            status_code=500,
            content=ApiResponse.create_response(ResponseCodeEnum.KOG01)
        )

@router.post('/update-user', response_model=ResponseDTO)
@inject
def update_user(
    update_user_dto: UpdateUserInput,
    user_usecase: UserUseCase = Depends(Provide[Container.user_usecase]),
    current_user: str = Depends(get_current_user)
) -> JSONResponse:
    """
    Actualiza los detalles de un usuario.

    Args:
        update_user_dto: Objeto con los datos a actualizar del usuario
        user_usecase: Caso de uso para operaciones de usuario
        current_user: Usuario actual autenticado

    Returns:
        JSONResponse: Respuesta con el resultado de la operación
    """
    logger.info("Iniciando actualización de usuario")
    try:
        validate_update_user(update_user_dto)
        user = map_update_user_dto_to_user(update_user_dto)
        user = user_usecase.update_user(user)
        response_data = map_user_to_user_output_dto(user).model_dump()
        return JSONResponse(
            status_code=200,
            content=ApiResponse.create_response(ResponseCodeEnum.KO000, response_data)
        )
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content=ApiResponse.create_response(ResponseCodeEnum.KOU06, str(e))
        )
    except CustomException as e:
        return JSONResponse(
            status_code=e.http_status,
            content=e.to_dict()
        )
    except Exception as e:
        logger.error(f"Excepción no manejada: {e}")
        return JSONResponse(
            status_code=500,
            content=ApiResponse.create_response(ResponseCodeEnum.KOG01)
        )
