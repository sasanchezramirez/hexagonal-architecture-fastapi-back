import logging
from typing import Final

from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from app.infrastructure.entry_point.dto.user_dto import NewUserInput, GetUser, LoginInput, UpdateUserInput
from app.infrastructure.entry_point.dto.response_dto import ResponseDTO
from app.application.container import Container
from app.domain.usecase.util.jwt import get_current_user
from app.infrastructure.entry_point.handler.auth_handler import AuthHandler

logger: Final[logging.Logger] = logging.getLogger("AuthController")

router: Final[APIRouter] = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/create-user', response_model=ResponseDTO, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    user_dto: NewUserInput,
    auth_handler: AuthHandler = Depends(Provide[Container.auth_handler])
) -> ResponseDTO:
    """
    Creates a new user in the system.
    """
    result = await auth_handler.create_user(user_dto)
    return ResponseDTO(
        apiCode="201",
        data=result,
        message="User created successfully",
        status=True
    )

@router.post('/get-user', response_model=ResponseDTO)
@inject
async def get_user(
    get_user_dto: GetUser,
    auth_handler: AuthHandler = Depends(Provide[Container.auth_handler]),
    current_user: dict = Depends(get_current_user)
) -> ResponseDTO:
    """
    Retrieves user details by ID or Email.
    """
    result = await auth_handler.get_user(get_user_dto, current_user.get('sub'))
    return ResponseDTO(
        apiCode="200",
        data=result,
        message="User retrieved successfully",
        status=True
    )

@router.post('/login', response_model=ResponseDTO)
@inject
async def login(
    login_dto: LoginInput,
    auth_handler: AuthHandler = Depends(Provide[Container.auth_handler])
) -> ResponseDTO:
    """
    Authenticates a user and generates an access token.
    """
    result = await auth_handler.login(login_dto)
    return ResponseDTO(
        apiCode="200",
        data=result,
        message="Login successful",
        status=True
    )

@router.post('/update-user', response_model=ResponseDTO)
@inject
async def update_user(
    update_user_dto: UpdateUserInput,
    auth_handler: AuthHandler = Depends(Provide[Container.auth_handler]),
    current_user: dict = Depends(get_current_user)
) -> ResponseDTO:
    """
    Updates user details.
    """
    result = await auth_handler.update_user(update_user_dto, current_user.get('sub'))
    return ResponseDTO(
        apiCode="200",
        data=result,
        message="User updated successfully",
        status=True
    )
