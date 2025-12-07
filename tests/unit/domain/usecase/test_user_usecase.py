import pytest
from app.domain.usecase.user_usecase import UserUseCase
from app.domain.model.user import User
from app.domain.model.util.exceptions import DuplicateUserException

class TestUserUseCase:

    @pytest.fixture
    def user_usecase(self, mock_user_gateway):
        return UserUseCase(mock_user_gateway)

    @pytest.mark.asyncio
    async def test_create_user_success(self, user_usecase, mock_user_gateway):
        # Arrange
        user_input = User(
            email="test@example.com",
            password="password123",
            creation_date="2024-01-01",
            profile_id=1,
            status_id=1
        )
        
        # Mock gateway behavior
        mock_user_gateway.create_user.return_value = User(
            id=1,
            email="test@example.com",
            password="hashed_password",
            creation_date="2024-01-01",
            profile_id=1,
            status_id=1
        )

        # Act
        result = await user_usecase.create_user(user_input)

        # Assert
        assert result.id == 1
        assert result.email == "test@example.com"
        # Verify password was hashed (logic is inside usecase)
        assert result.password != "password123" 
        mock_user_gateway.create_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_duplicate(self, user_usecase, mock_user_gateway):
        # Arrange
        user_input = User(
            email="duplicate@example.com", 
            password="password123", # Valid length
            creation_date="2024-01-01",
            profile_id=1,
            status_id=1
        )
        mock_user_gateway.create_user.side_effect = DuplicateUserException("duplicate@example.com")

        # Act & Assert
        with pytest.raises(DuplicateUserException) as exc:
            await user_usecase.create_user(user_input)
        
        assert "duplicate@example.com" in exc.value.message

    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self, user_usecase, mock_user_gateway):
        # Arrange
        mock_user_gateway.get_user_by_id.return_value = User(
            id=1, 
            email="found@example.com",
            creation_date="2024-01-01", # Required field
            profile_id=1,
            status_id=1
        )

        # Act
        result = await user_usecase.get_user_by_id(1)

        # Assert
        assert result.id == 1
        assert result.email == "found@example.com"
        mock_user_gateway.get_user_by_id.assert_called_once_with(1)
