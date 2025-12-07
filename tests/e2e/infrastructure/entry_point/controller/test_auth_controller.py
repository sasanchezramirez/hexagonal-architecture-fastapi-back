import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from app.infrastructure.entry_point.dto.user_dto import UserOutput

class TestAuthController:

    @pytest.mark.asyncio
    async def test_create_user_success(self, app):
        # Arrange
        mock_auth_handler = AsyncMock()
        mock_auth_handler.create_user.return_value = UserOutput(
            id=1,
            email="test@example.com",
            creation_date="2024-01-01",
            profile_id=1,
            status_id=1
        )

        user_input = {
            "email": "test@example.com",
            "password": "password123",
            "profile_id": 1,
            "status_id": 1
        }

        # Act
        with app.container.auth_handler.override(mock_auth_handler):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post("/auth/create-user", json=user_input)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["apiCode"] == "201"
        assert data["data"]["email"] == "test@example.com"
        assert data["status"] is True

    @pytest.mark.asyncio
    async def test_create_user_validation_error(self, app):
        # Arrange
        user_input = {
            "email": "invalid-email", # Invalid email
            "password": "short", # Too short
            "profile_id": 1,
            "status_id": 1
        }

        # Act
        # No need to mock handler as validation happens before
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/auth/create-user", json=user_input)

        # Assert
        assert response.status_code == 422
        data = response.json()
        assert data["apiCode"] == "422"
        assert data["status"] is False
        assert "errors" in data["data"]
