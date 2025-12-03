# Backend Archetype with FastAPI and Hexagonal Architecture

![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![Architecture](https://img.shields.io/badge/Hexagonal-Architecture-purple.svg)

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
5.  [Development Guidelines](#development-guidelines)
    *   [How to Add a New Endpoint](#how-to-add-a-new-endpoint)
    *   [How to Add a New Use Case](#how-to-add-a-new-use-case)
    *   [How to Change the Database Engine](#how-to-change-the-database-engine)
6.  [Key Concepts Implemented](#key-concepts-implemented)
    *   [Dependency Injection](#dependency-injection)
    *   [Exception Handling](#exception-handling)
7.  [API Endpoints Guide](#api-endpoints-guide)

---

## 1. Philosophy and Architectural Approach

### Hexagonal Architecture (Ports and Adapters)

The core of this archetype is the separation of concerns. We visualize the business logic as a central "hexagon" that must not depend on anything external.

-   **Inside the Hexagon (`domain`):** Contains pure business logic (models, use cases) and the interfaces it needs to communicate with the outside world (the "Ports", such as `PersistenceGateway`). It doesn't know if the app is a web API or a console app.
-   **Outside the Hexagon (`infrastructure`):** Contains the "Adapters" that implement the ports and connect the domain to the real world.
    -   **Primary Adapters (Driving Adapters):** Drive the application. In our case, the FastAPI handlers (`infrastructure/entry_point`) that receive HTTP requests.
    -   **Secondary Adapters (Driven Adapters):** Are driven by the application. Our persistence layer (`infrastructure/driven_adapter`) implements the `PersistenceGateway` using SQLAlchemy.

### Request Flow

A `POST` request to `/auth/create-user` follows this path:

1.  **EntryPoint (Primary Adapter):** The handler in `auth.py` receives the HTTP request, validates it using a DTO and manual validators, and calls the `UserUseCase`.
2.  **UseCase (Domain):** The `create_user` method in `UserUseCase` executes business logic (hashing password, etc.) and calls the `create_user` method of the `PersistenceGateway` port.
3.  **Gateway (Domain Port):** The `PersistenceGateway` is an abstract interface. The use case doesn't know who implements it.
4.  **Persistence (Secondary Adapter):** The `Persistence` class in `persistence.py`, which implements the gateway, receives the call. It acts as a proxy/orchestrator for the `UserRepository` and mappers, converting domain models into DB entities.
5.  **Repository (Infrastructure):** The `UserRepository` executes the final operation against the database using SQLAlchemy.

### The Power of Async

The entire application, from endpoints to database calls, uses `async/await`. This means that when an I/O operation (like a DB query) is waiting, the server doesn't block. It yields control to handle other concurrent requests. This allows for performance and scalability far superior to a traditional synchronous approach with a single process.

---

## 2. Project Structure

```
app/
├── application/      # Orchestration: Dependency injection, config, app startup.
├── domain/           # The business core. Zero infrastructure dependencies.
│   ├── gateway/      # Ports: Interfaces the domain needs (e.g., for persistence).
│   ├── model/        # Business models (Pydantic) and domain exceptions.
│   └── usecase/      # Business logic and workflow orchestration.
└── infrastructure/   # Everything external: frameworks, databases, etc.
    ├── driven_adapter/ # Adapters "driven" by the domain (e.g., DB, external APIs).
    │   └── persistence/ # Contains the Persistence proxy and Repositories.
    └── entry_point/    # Adapters that "drive" the domain (e.g., API handlers).
```

---

## 3. Getting Started

### Prerequisites
-   Python 3.11+
-   A running PostgreSQL instance
-   Docker (optional, for DB)

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

## 5. Development Guidelines

### How to Add a New Endpoint
1.  **Create the DTO:** Define input/output models in `app/infrastructure/entry_point/dto/`.
2.  **Create the Mapper:** Add functions in `app/infrastructure/entry_point/mapper/` to convert between DTO and domain model.
3.  **Add the Endpoint:** In the corresponding handler file in `app/infrastructure/entry_point/handler/`, add the new route using the `@router` decorator.
4.  **Call the Use Case:** Inject and call the appropriate use case. The handler manages routing logic (HTTP -> Domain).

### How to Add a New Use Case
1.  **Define the Use Case:** Create a new class in `app/domain/usecase/`. It must receive its dependencies (like `PersistenceGateway`) in the constructor.
2.  **Implement Logic:** Write methods containing pure business logic.
3.  **Register in Container:** In `app/application/container.py`, add a new `provider.Factory` for your use case, injecting its dependencies.

### How to Change the Database Engine
Thanks to the decoupled architecture, this process is simple:
1.  **Install Async Driver:** Install the necessary driver for your new database (e.g., `pip install aiomysql` for MySQL).
2.  **Update Connection URL:** In your `.env` file, modify `DATABASE_URL` to point to the new database and use the new driver.
3.  **Done!** No other code changes are needed, as the domain layer and use cases are unaware of the database implementation.

---

## 6. Key Concepts Implemented

### Dependency Injection
We use the `dependency-injector` library. The `app/application/container.py` file acts as the application's "blueprint," defining how classes (`Persistence`, `UserUseCase`, etc.) are constructed and connected without them knowing each other directly. This is fundamental for decoupling and testability.

### Exception Handling
The project uses a global and centralized exception handling system. Semantic business exceptions (e.g., `UserNotFoundException`) are raised from internal layers and caught by specific handlers in the API layer, which translate them into standardized HTTP responses. This keeps endpoints clean and the domain agnostic to HTTP.

---

## 7. API Endpoints Guide

| Verb   | Route               | Description                      | Auth Required |
| :----- | :------------------ | :------------------------------- | :------------ |
| `POST` | `/auth/create-user` | Creates a new user.              | No            |
| `POST` | `/auth/login`       | Authenticates and returns JWT.   | No            |
| `POST` | `/auth/get-user`    | Gets a user by ID or email.      | Yes           |
| `POST` | `/auth/update-user` | Updates an existing user.        | Yes           |

---

## 8. Database Schema

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
