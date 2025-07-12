class DomainException(Exception):
    """Clase base para excepciones específicas del dominio."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class UserNotFoundException(DomainException):
    """Lanzada cuando un usuario no se encuentra en la capa de persistencia."""
    def __init__(self, user_id: int = None, email: str = None):
        if user_id:
            message = f"Usuario con ID '{user_id}' no encontrado."
        elif email:
            message = f"Usuario con email '{email}' no encontrado."
        else:
            message = "Usuario no encontrado."
        super().__init__(message)

class DuplicateUserException(DomainException):
    """Lanzada al intentar crear un usuario que ya existe."""
    def __init__(self, email: str):
        message = f"Un usuario con el email '{email}' ya existe."
        super().__init__(message)

class InvalidCredentialsException(DomainException):
    """Lanzada cuando las credenciales de autenticación son inválidas."""
    def __init__(self):
        message = "Credenciales inválidas proporcionadas."
        super().__init__(message)

class InvalidTokenException(DomainException):
    """Lanzada cuando un token JWT es inválido."""
    def __init__(self, message: str = "Token de autenticación inválido."):
        super().__init__(message)

class ExpiredTokenException(InvalidTokenException):
    """Lanzada cuando un token JWT ha expirado."""
    def __init__(self):
        super().__init__("El token de autenticación ha expirado.")

class PersistenceException(DomainException):
    """Lanzada para errores de persistencia genéricos y no especificados."""
    def __init__(self, original_exception: Exception = None):
        message = "Ocurrió un error inesperado en la capa de persistencia."
        self.original_exception = original_exception
        super().__init__(message)
