import logging
from typing import Final

from app.domain.model.user import User
from app.domain.model.util.exceptions import InvalidCredentialsException
from app.domain.gateway.user_data_gateway import IUserDataGateway
from app.domain.usecase.util.security import verify_password
from app.domain.usecase.util.jwt import create_access_token


logger: Final[logging.Logger] = logging.getLogger("AuthUseCase")


class AuthUseCase:
    """
    Use case for user authentication.
    
    This class handles business logic related to user authentication,
    including credential verification and access token generation.
    """

    def __init__(self, user_data_gateway: IUserDataGateway) -> None:
        """
        Initializes the authentication use case.
        """
        self.user_data_gateway: Final[IUserDataGateway] = user_data_gateway

    async def authenticate_user(self, user: User) -> str:
        """
        Authenticates a user and generates an access token if credentials are valid.

        Args:
            user: User to authenticate with credentials.

        Returns:
            str: Access token if authentication is successful.
        
        Raises:
            InvalidCredentialsException: If email is not found or password is incorrect.
        """
        logger.info(f"Starting authentication for user: {user.email}")
        
        db_user = await self.user_data_gateway.get_user_by_email(user.email)
        
        if not db_user or not verify_password(user.password, db_user.password):
            logger.warning(f"Authentication failed for: {user.email}")
            raise InvalidCredentialsException()
            
        logger.info(f"Authentication successful for: {user.email}")
        return create_access_token({"sub": db_user.email})



            

