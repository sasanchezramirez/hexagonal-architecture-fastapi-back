class DomainException(Exception):
    """Base class for domain-specific exceptions."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class UserNotFoundException(DomainException):
    """Raised when a user is not found in the persistence layer."""
    def __init__(self, user_id: int = None, email: str = None):
        if user_id:
            message = f"User with ID '{user_id}' not found."
        elif email:
            message = f"User with email '{email}' not found."
        else:
            message = "User not found."
        super().__init__(message)

class DuplicateUserException(DomainException):
    """Raised when attempting to create a user that already exists."""
    def __init__(self, email: str):
        message = f"A user with email '{email}' already exists."
        super().__init__(message)

class InvalidCredentialsException(DomainException):
    """Raised when authentication credentials are invalid."""
    def __init__(self):
        message = "Invalid credentials provided."
        super().__init__(message)

class InvalidTokenException(DomainException):
    """Raised when a JWT token is invalid."""
    def __init__(self, message: str = "Invalid authentication token."):
        super().__init__(message)

class ExpiredTokenException(InvalidTokenException):
    """Raised when a JWT token has expired."""
    def __init__(self):
        super().__init__("The authentication token has expired.")

class PersistenceException(DomainException):
    """Raised for generic and unspecified persistence errors."""
    def __init__(self, original_exception: Exception = None):
        message = "An unexpected error occurred in the persistence layer."
        self.original_exception = original_exception
        super().__init__(message)
