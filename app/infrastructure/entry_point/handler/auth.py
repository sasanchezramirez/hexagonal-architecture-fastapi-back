import  app.infrastructure.entry_point.validator.validator as validator
import app.infrastructure.entry_point.mapper.user_mapper as user_mapper
import logging

from fastapi import APIRouter, Depends 
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from app.infrastructure.entry_point.dto.user_dto import NewUserInput, GetUser
from app.domain.usecase.user_usecase import UserUseCase
from app.application.container import Container
from app.domain.model.util.custom_exceptions import CustomException

from app.domain.model.util.response_codes import ResponseCodeEnum
from app.infrastructure.entry_point.dto.response_dto import ResponseDTO
from app.infrastructure.entry_point.utils.api_response import ApiResponse



logger = logging.getLogger("Auth Handler")

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/create-user', 
    response_model=ResponseDTO,
    responses={
        200: {"description": "Operation successful", "model": ResponseDTO},
        400: {"description": "Validation Error", "model": ResponseDTO},
        500: {"description": "Internal Server Error", "model": ResponseDTO},
    }
)
@inject
def create_user(
    user_dto: NewUserInput,
    user_usecase: UserUseCase = Depends(Provide[Container.user_usecase])
):
    """
    Crea un nuevo usuario en el sistema
    
    Args:
        user_dto (NewUserInput): El objeto de transferencia de datos que contiene los detalles del usuario.
        user_usecase (UserUseCase): El UseCase del User.

    Returns:
        ResponseDTO: Un objeto de respuesta con los datos de la operación.
    """
    
    logger.info("Init create-user handler")
    try:
        validator.validate_new_user(user_dto)
    except ValueError as e:
        response_code = ApiResponse.create_response(ResponseCodeEnum.KOD01, str(e))
        return  JSONResponse(status_code=400, content=response_code)


    user = user_mapper.map_user_dto_to_user(user_dto)

    try:
        user = user_usecase.create_user(user)
        response_data = user_mapper.map_user_to_user_output_dto(user)
        return ApiResponse.create_response(ResponseCodeEnum.KO000, response_data)
    except CustomException as e:
        response_code = e.to_dict()
        return  JSONResponse(status_code=e.http_status, content=response_code)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        response_code = ApiResponse.create_response(ResponseCodeEnum.KOG01)
        return JSONResponse(status_code=500, content=response_code)
    

@router.post(
    '/get-user',
    response_model=ResponseDTO,
    responses={
        200: {"description": "Operation successful", "model": ResponseDTO},
        400: {"description": "Validation Error", "model": ResponseDTO},
        404: {"description": "User Not Found", "model": ResponseDTO},
        500: {"description": "Internal Server Error", "model": ResponseDTO},
    }
)
@inject
def get_user(
    get_user_dto: GetUser,
    user_usecase: UserUseCase = Depends(Provide(Container.user_usecase))
):
    """
    Obtiene los detalles del usuario.

    Args:
        get_user_dto (GetUser): El objeto de transferencia de datos que contiene los detalles necesarios del usuario.
        user_usecase (UserUseCase): El UseCase del User.

    Returns:
        ResponseDTO: Un objeto de respuesta con los datos del usuario.
    """
    logger.info("Init get-user handler")
    try:
        validator.validate_get_user(get_user_dto)
    except ValueError as e:
        response_code = ApiResponse.create_response(ResponseCodeEnum.KOD01, str(e))
        return  JSONResponse(status_code=400, content=response_code)
    
    user = user_mapper.map_get_user_dto_to_user(get_user_dto)

    try:
        user = user_usecase.get_user(user)
        response_data = user_mapper.map_user_to_user_output_dto(user)
        return ApiResponse.create_response(ResponseCodeEnum.KO000, response_data)
    except CustomException as e:
        response_code = e.to_dict()
        return  JSONResponse(status_code=e.http_status, content=response_code)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        response_code = ApiResponse.create_response(ResponseCodeEnum.KOG01)
        return JSONResponse(status_code=500, content=response_code)
    