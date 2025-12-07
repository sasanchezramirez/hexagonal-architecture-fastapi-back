# Backend Archetype with FastAPI and Hexagonal Architecture

![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![Architecture](https://img.shields.io/badge/Hexagonal-Architecture-purple.svg)
![Testing](https://img.shields.io/badge/Testing-Pytest-yellow.svg)

An asynchronous RESTful API built with Python and FastAPI, following **Hexagonal Architecture (Ports and Adapters)** principles to achieve high decoupling, maintainability, and testability.

This project serves as a professional-level archetype for building robust backend services. Its goal is to demonstrate how to structure an application so that the core business logic remains isolated from infrastructure decisions (like the web framework or database), allowing it to evolve independently.

---

## Table of Contents

1.  [Philosophy and Architectural Approach](#philosophy-and-architectural-approach)
    *   [Hexagonal Architecture (Ports and Adapters)](#hexagonal-architecture-ports-and-adapters)
    *   [Request Flow](#request-flow)
    *   [The Power of Async](#the-power-of-async)
2.  [Project Structure](#project-structure)
3.  [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
4.  [Running the Application](#running-the-application)
5.  [Testing](#testing)
6.  [Development Guidelines](#development-guidelines)
    *   [How to Add a New Endpoint](#how-to-add-a-new-endpoint)
    *   [How to Add a New Use Case](#how-to-add-a-new-use-case)
7.  [Key Concepts Implemented](#key-concepts-implemented)
    *   [Dependency Injection](#dependency-injection)
    *   [Exception Handling](#exception-handling)
    *   [Validation](#validation)
8.  [API Endpoints Guide](#api-endpoints-guide)

---

## 1. Philosophy and Architectural Approach

### Hexagonal Architecture (Ports and Adapters)

The core of this archetype is the separation of concerns. We visualize the business logic as a central "hexagon" that must not depend on anything external.

-   **Inside the Hexagon (`domain`):** Contains pure business logic (models, use cases) and the interfaces it needs to communicate with the outside world (the "Ports", such as `IUserDataGateway`). It doesn't know if the app is a web API or a console app.
-   **Outside the Hexagon (`infrastructure`):** Contains the "Adapters" that implement the ports and connect the domain to the real world.
    -   **Primary Adapters (Driving Adapters):** Drive the application. In our case, the FastAPI handlers (`infrastructure/entry_point`) that receive HTTP requests.
    -   **Secondary Adapters (Driven Adapters):** Are driven by the application. Our persistence layer (`infrastructure/driven_adapter`) implements the `IUserDataGateway` using SQLAlchemy.

### Request Flow

A `POST` request to `/auth/create-user` follows this path:

1.  **EntryPoint (Primary Adapter):** The `AuthController` receives the HTTP request. Pydantic DTOs automatically validate the input format.
2.  **UseCase (Domain):** The `UserUseCase` executes business logic (e.g., hashing password) and calls the `create_user` method of the `IUserDataGateway` port.
3.  **Gateway (Domain Port):** The `IUserDataGateway` is an abstract interface. The use case doesn't know who implements it.
4.  **Persistence (Secondary Adapter):** The `UserDataGatewayImpl` implements the interface. It uses the `UserRepository` to interact with the database.
5.  **Repository (Infrastructure):** The `UserRepository` executes the final operation against the database using SQLAlchemy (Async).

### The Power of Async

The entire application, from endpoints to database calls, uses `async/await`. This means that when an I/O operation (like a DB query) is waiting, the server doesn't block. It yields control to handle other concurrent requests. This allows for performance and scalability far superior to a traditional synchronous approach with a single process.

---

## 2. Project Structure

```
app/
├── application/      # Orchestration: Dependency injection, config, app startup.
├── domain/           # The business core. Zero infrastructure dependencies.
│   ├── gateway/      # Ports: Interfaces the domain needs (e.g., IUserDataGateway).
│   ├── model/        # Business models (Pydantic) and domain exceptions.
│   └── usecase/      # Business logic and workflow orchestration.
└── infrastructure/   # Everything external: frameworks, databases, etc.
    ├── driven_adapter/ # Adapters "driven" by the domain (e.g., DB, external APIs).
    │   ├── persistence/ # Contains Repositories and DB configuration.
    │   └── user_adapter/ # Implementation of Domain Gateways.
    └── entry_point/    # Adapters that "drive" the domain (e.g., API handlers).
        ├── controller/ # FastAPI Routers.
        ├── dto/        # Data Transfer Objects with Pydantic validation.
        └── handler/    # Logic to bridge Controller and UseCase.
```

---

## 3. Getting Started

### Prerequisites
-   Python 3.11+
-   A running PostgreSQL instance (or Docker)

### Installation
1.  **Clone the repository:** `git clone <URL>`
2.  **Create a virtual environment:** `python -m venv .venv && source .venv/bin/activate`
3.  **Install dependencies:** `pip install -r requirements.txt`
4.  **Configure environment:** Copy `.env.example` to `.env` and edit it with your database credentials.

---

## 4. Running the Application

```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000/docs`.

---

## 5. Testing

The project includes a comprehensive testing suite using `pytest`.

### Running Tests
```bash
pytest
```

### Test Structure
-   **Unit Tests (`tests/unit`):** Verify business logic in Use Cases, mocking external dependencies.
-   **E2E Tests (`tests/e2e`):** Verify API endpoints and integration using `TestClient`.

---

## 6. Development Guidelines

### How to Add a New Endpoint
1.  **Create the DTO:** Define input/output models in `app/infrastructure/entry_point/dto/` using Pydantic v2.
2.  **Create the Mapper:** Add functions in `app/infrastructure/entry_point/mapper/` to convert between DTO and domain model.
3.  **Add the Controller:** In `app/infrastructure/entry_point/controller/`, define the route and call the Handler.
4.  **Add the Handler:** In `app/infrastructure/entry_point/handler/`, implement the logic to call the Use Case.

### How to Add a New Use Case
1.  **Define the Use Case:** Create a new class in `app/domain/usecase/`. It must receive its dependencies (like `IUserDataGateway`) in the constructor.
2.  **Implement Logic:** Write methods containing pure business logic.
3.  **Register in Container:** In `app/application/container.py`, add a new `provider.Factory` for your use case, injecting its dependencies.

---

## 7. Key Concepts Implemented

### Dependency Injection
We use the `dependency-injector` library. The `app/application/container.py` file acts as the application's "blueprint," defining how classes are constructed and connected without them knowing each other directly. This is fundamental for decoupling and testability.

### Exception Handling
The project uses a global and centralized exception handling system. Semantic business exceptions (e.g., `UserNotFoundException`) are raised from internal layers and caught by specific handlers in the API layer, which translate them into standardized HTTP responses (`ResponseDTO`).

### Validation
Data validation is handled declaratively using **Pydantic v2**. DTOs define the expected structure and constraints (e.g., `EmailStr`, `min_length`), ensuring that invalid data never reaches the domain layer.

---

## 8. API Endpoints Guide

| Verb   | Route               | Description                      | Auth Required |
| :----- | :------------------ | :------------------------------- | :------------ |
| `POST` | `/auth/create-user` | Creates a new user.              | No            |
| `POST` | `/auth/login`       | Authenticates and returns JWT.   | No            |
| `POST` | `/auth/get-user`    | Gets a user by ID or email.      | Yes           |
| `POST` | `/auth/update-user` | Updates an existing user.        | Yes           |

---

## 9. Database Schema

Here are the SQL queries to create the database entities:

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    creation_date VARCHAR NOT NULL,
    profile_id INTEGER,
    status_id INTEGER
);

CREATE UNIQUE INDEX ix_users_email ON users (email);
```
