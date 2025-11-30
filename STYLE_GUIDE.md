# Project Style Guide

This document defines the engineering standards, coding conventions, and best practices for the project.

## 1. Naming Conventions

We follow **PEP 8** standards with specific rules for our hexagonal architecture.

### 1.1. Files and Directories
- **Snake Case (`snake_case`)**: Used for all file and directory names.
- **Descriptive Suffixes**: Files must indicate their architectural role.
    - `user_usecase.py` (Not just `user.py`)
    - `user_repository.py`
    - `user_dto.py`
    - `user_entity.py`

### 1.2. Classes
- **Pascal Case (`PascalCase`)**: Used for class names.
- **Role Suffixes**: Class names must match the filename (without underscores).
    - `UserUseCase`
    - `UserRepository`
    - `UserEntity`

### 1.3. Variables and Functions
- **Snake Case (`snake_case`)**: Used for variables, functions, and methods.
- **Constants**: `UPPER_CASE_WITH_UNDERSCORES`.
- **Private Members**: Use `_` prefix for internal methods/attributes (e.g., `_validate_internal_state`).

### 1.4. Specific Variable Names
- **Database Session**: Use `session` (avoid `db`, `conn`).
- **Entities (ORM)**: Use `_entity` suffix or clear context (e.g., `user_entity`).
- **Domain Models**: Clean names (e.g., `user`).
- **DTOs**: Explicit suffix if needed, or clear context (e.g., `user_create_dto`).

## 2. Code Style & Formatting

### 2.1. Type Hinting
- **Strict Typing**: All function signatures must have type hints.
- **Return Types**: Always specify return types, including `-> None`.

```python
def get_user(self, user_id: int) -> Optional[User]:
    ...
```

### 2.2. Docstrings
- **Google Style**: Use Google-style docstrings for all public classes and methods.
- **Content**: Include `Args`, `Returns`, and `Raises` sections.

```python
def calculate_total(self, price: float, tax: float) -> float:
    """
    Calculates the total price including tax.

    Args:
        price: The base price.
        tax: The tax rate.

    Returns:
        float: The final total price.
    """
    ...
```

## 3. Logging Standards

### 3.1. Levels
- **INFO**: High-level flow events (e.g., "User creation started").
- **WARNING**: Recoverable issues or unexpected inputs (e.g., "Login failed").
- **ERROR**: Unhandled exceptions or external service failures.

### 3.2. Format
- **Structured Logging**: Logs should be structured (JSON preferred in production).
- **Context**: Always include relevant context (IDs, operation names).

```python
logger.info("User created", extra={"user_id": 123})
```

## 4. Exception Handling Style

### 4.1. Hierarchy
- **Domain Exceptions**: Base class for business logic errors.
- **Infrastructure Exceptions**: Base class for technical errors (DB, Network).

### 4.2. Usage
- **No Empty Excepts**: Never use bare `except:`. Always catch specific exceptions.
- **Propagation**: Do not catch exceptions just to log them and re-raise immediately without adding context.
