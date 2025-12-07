import pytest
from unittest.mock import AsyncMock
from app.domain.gateway.user_data_gateway import IUserDataGateway
from app.application.fast_api import create_app

@pytest.fixture
def mock_user_gateway():
    """
    Fixture that returns a mock of IUserDataGateway.
    """
    gateway = AsyncMock(spec=IUserDataGateway)
    return gateway

@pytest.fixture
def app():
    """
    Fixture that returns the FastAPI application.
    """
    return create_app()
