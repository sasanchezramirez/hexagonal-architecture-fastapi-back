# Arquetipo de Backend con FastAPI y Arquitectura Hexagonal

![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![Arquitectura](https://img.shields.io/badge/Arquitectura-Hexagonal-purple.svg)

API RESTful asíncrona construida con Python y FastAPI, siguiendo los principios de la Arquitectura Hexagonal (Puertos y Adaptadores) para lograr un alto desacoplamiento, mantenibilidad y testeabilidad.

Este proyecto sirve como un arquetipo de nivel profesional para construir servicios de backend robustos. Su objetivo es demostrar cómo estructurar una aplicación para que la lógica de negocio central permanezca aislada de las decisiones de infraestructura (como el framework web o la base de datos), permitiendo que evolucione de forma independiente.

---

## Tabla de Contenidos

1.  [Filosofía y Enfoque Arquitectónico](#filosofía-y-enfoque-arquitectónico)
    *   [Arquitectura Hexagonal (Puertos y Adaptadores)](#arquitectura-hexagonal-puertos-y-adaptadores)
    *   [Flujo de una Petición](#flujo-de-una-petición)
    *   [El Poder del Enfoque Asíncrono](#el-poder-del-enfoque-asíncrono)
2.  [Estructura del Proyecto](#estructura-del-proyecto)
3.  [Primeros Pasos](#primeros-pasos)
    *   [Prerrequisitos](#prerrequisitos)
    *   [Instalación](#instalación)
4.  [Ejecutar la Aplicación](#ejecutar-la-aplicación)
5.  [Guías Prácticas de Desarrollo](#guías-prácticas-de-desarrollo)
    *   [Cómo Añadir un Nuevo Endpoint](#cómo-añadir-un-nuevo-endpoint)
    *   [Cómo Añadir un Nuevo Caso de Uso](#cómo-añadir-un-nuevo-caso-de-uso)
    *   [Cómo Cambiar el Motor de Base de Datos](#cómo-cambiar-el-motor-de-base-de-datos)
    *   [Cómo Añadir un Nuevo Adaptador (Driven Adapter)](#cómo-añadir-un-nuevo-adaptador-driven-adapter)
    *   [Cómo Añadir una Nueva Excepción de Negocio](#cómo-añadir-una-nueva-excepción-de-negocio)
6.  [Conceptos Clave Implementados](#conceptos-clave-implementados)
    *   [Inyección de Dependencias](#inyección-de-dependencias)
    *   [Manejo de Excepciones](#manejo-de-excepciones)
7.  [Guía de Endpoints de la API](#guía-de-endpoints-de-la-api)
8.  [Testing](#testing)

---

## 1. Filosofía y Enfoque Arquitectónico

### Arquitectura Hexagonal (Puertos y Adaptadores)

El núcleo de este arquetipo es la separación de responsabilidades. Imaginamos la lógica de negocio como un "hexágono" central que no debe depender de nada externo.

-   **El Interior del Hexágono (`domain`):** Contiene la lógica de negocio pura (modelos, casos de uso) y las interfaces que necesita para comunicarse con el exterior (los "Puertos", como `PersistenceGateway`). No sabe si la app es una API web o una app de consola.
-   **El Exterior del Hexágono (`infrastructure`):** Contiene los "Adaptadores" que implementan los puertos y conectan el dominio con el mundo real.
    -   **Adaptadores Primarios (Driving Adapters):** Impulsan la aplicación. En nuestro caso, los handlers de FastAPI (`infrastructure/entry_point`) que reciben peticiones HTTP.
    -   **Adaptadores Secundarios (Driven Adapters):** Son impulsados por la aplicación. Nuestra capa de persistencia (`infrastructure/driven_adapter`) que implementa el `PersistenceGateway` usando SQLAlchemy.

![Hexagonal Architecture Diagram](https://i.imgur.com/y3b4s1A.png)

### Flujo de una Petición

Un `POST` a `/auth/create-user` sigue este camino:
1.  **EntryPoint (Adaptador Primario):** El handler en `auth.py` recibe la petición HTTP, la valida usando un DTO y llama al `UserUseCase`.
2.  **UseCase (Dominio):** El `create_user` en `UserUseCase` ejecuta la lógica de negocio (hashear contraseña, etc.) y llama al método `create_user` del puerto `PersistenceGateway`.
3.  **Gateway (Puerto del Dominio):** El `PersistenceGateway` es una interfaz abstracta. El caso de uso no sabe quién la implementa.
4.  **Persistence (Adaptador Secundario):** La clase `Persistence` en `persistence.py`, que implementa el gateway, recibe la llamada. Orquesta al `UserRepository` y a los mappers para convertir el modelo de dominio en una entidad de BD.
5.  **Repository (Infraestructura):** El `UserRepository` ejecuta la operación final contra la base de datos usando SQLAlchemy.

### El Poder del Enfoque Asíncrono

Toda la aplicación, desde los endpoints hasta las llamadas a la base de datos, utiliza `async/await`. Esto significa que cuando una operación de I/O (como una consulta a la BD) está en espera, el servidor no se bloquea. Cede el control para atender otras peticiones concurrentemente. Esto permite un rendimiento y una escalabilidad muy superiores a los de un enfoque síncrono tradicional con un solo proceso.

---

## 2. Estructura del Proyecto

```
app/
├── application/      # Orquestación: Inyección de dependencias, configuración, arranque de la app.
├── domain/           # El núcleo del negocio. Cero dependencias de infraestructura.
│   ├── gateway/      # Puertos: Interfaces que el dominio necesita (ej. para persistencia).
│   ├── model/        # Modelos de negocio (Pydantic) y excepciones de dominio.
│   └── usecase/      # Lógica de negocio y orquestación de los flujos de trabajo.
└── infrastructure/   # Todo lo externo: frameworks, bases de datos, etc.
    ├── driven_adapter/ # Adaptadores "impulsados" por el dominio (ej. BD, APIs externas).
    │   └── persistence/
    └── entry_point/    # Adaptadores que "impulsan" el dominio (ej. handlers de API).
```

---

## 3. Primeros Pasos

### Prerrequisitos
-   Python 3.11+
-   Una instancia de PostgreSQL en ejecución
-   Docker (opcional, para la BD)

### Instalación
1.  **Clona el repositorio:** `git clone <URL>`
2.  **Crea un entorno virtual:** `python -m venv .venv && source .venv/bin/activate`
3.  **Instala dependencias:** `pip install -r requirements.txt`
4.  **Configura el entorno:** Copia `.env.example` a `.env` y edítalo con tus credenciales de base de datos.

---

## 4. Ejecutar la Aplicación

```bash
uvicorn app.main:app --reload
```
La API estará disponible en `http://127.0.0.1:8000/docs`.

---

## 5. Guías Prácticas de Desarrollo

### Cómo Añadir un Nuevo Endpoint
1.  **Crea el DTO:** Define los modelos de entrada/salida en un archivo dentro de `app/infrastructure/entry_point/dto/`.
2.  **Crea el Mapper:** Si es necesario, añade funciones en `app/infrastructure/entry_point/mapper/` para convertir entre el DTO y el modelo de dominio.
3.  **Añade el Endpoint:** En el archivo de handler correspondiente en `app/infrastructure/entry_point/handler/`, añade la nueva ruta usando el decorador `@router`.
4.  **Llama al Caso de Uso:** Inyecta y llama al caso de uso apropiado. El handler se encarga de la lógica de enrutamiento (HTTP -> Dominio).

### Cómo Añadir un Nuevo Caso de Uso
1.  **Define el Caso de Uso:** Crea una nueva clase en `app/domain/usecase/`. Debe recibir sus dependencias (como el `PersistenceGateway`) en el constructor.
2.  **Implementa la Lógica:** Escribe los métodos que contienen la lógica de negocio pura.
3.  **Regístralo en el Contenedor:** En `app/application/container.py`, añade un nuevo `provider.Factory` para tu caso de uso, inyectándole sus dependencias.

### Cómo Cambiar el Motor de Base de Datos
Gracias a la arquitectura desacoplada, este proceso es sorprendentemente simple.
1.  **Instala el Driver Asíncrono:** Instala el driver necesario para tu nueva base de datos (ej. `pip install aiomysql` para MySQL).
2.  **Actualiza la URL de Conexión:** En tu archivo `.env`, modifica la `DATABASE_URL` para que apunte a la nueva base de datos y use el nuevo driver (ej. `DATABASE_URL="mysql+aiomysql://user:pass@host/db"`).
3.  **¡Listo!** No es necesario cambiar ningún otro código, ya que la capa de dominio y los casos de uso no tienen conocimiento de la implementación de la base de datos.

### Cómo Añadir un Nuevo Adaptador (Driven Adapter)
Imagina que necesitas notificar por email cuando un usuario se crea.
1.  **Define el Puerto en el Dominio:** En `app/domain/gateway/`, crea una nueva interfaz:
    ```python
    class NotificationGateway(ABC):
        @abstractmethod
        async def send_welcome_email(self, user: User):
            pass
    ```
2.  **Actualiza el Caso de Uso:** Inyecta el nuevo gateway en el `UserUseCase` y llámalo en `create_user`.
3.  **Crea el Adaptador en Infraestructura:** En `app/infrastructure/driven_adapter/`, crea una nueva carpeta `notification/` y dentro un archivo `email_service.py`:
    ```python
    class EmailService(NotificationGateway):
        async def send_welcome_email(self, user: User):
            # Lógica para conectar a un servicio como SendGrid y enviar el email
            print(f"Enviando email de bienvenida a {user.email}")
    ```
4.  **Regístralo en el Contenedor:** En `container.py`, añade un nuevo `provider` para `EmailService` y actualiza el `provider` del `UserUseCase` para inyectarle la nueva dependencia.

### Cómo Añadir una Nueva Excepción de Negocio
Sigue el patrón de **Nacimiento -> Burbujeo -> Traducción**.
1.  **Definir la Excepción:** En `app/domain/model/util/exceptions.py`, crea una nueva clase que herede de `DomainException`.
2.  **Lanzar la Excepción:** En la capa que tiene el contexto para detectar el error (normalmente un `UseCase` o un `Adapter`), lanza tu nueva excepción.
3.  **Crear el Manejador:** En `app/infrastructure/entry_point/utils/exception_handler.py`, crea una función `async` que reciba la excepción y devuelva una `JSONResponse` con el código de estado y mensaje apropiados.
4.  **Registrar el Manejador:** En `app/application/fast_api.py`, usa `app.add_exception_handler()` para registrar tu nuevo manejador. Recuerda hacerlo antes de los manejadores más genéricos.

---

## 6. Conceptos Clave Implementados

### Inyección de Dependencias
Utilizamos la librería `dependency-injector`. El archivo `app/application/container.py` actúa como el "plano" de la aplicación, definiendo cómo se construyen y conectan las clases (`Persistence`, `UserUseCase`, etc.) sin que ellas se conozcan directamente. Esto es fundamental para el desacoplamiento y la testeabilidad.

### Manejo de Excepciones
El proyecto utiliza un sistema de manejo de excepciones global y centralizado. Las excepciones semánticas de negocio (ej. `UserNotFoundException`) se lanzan desde las capas internas y son capturadas por manejadores específicos en la capa de la API, que las traducen a respuestas HTTP estandarizadas. Esto mantiene los endpoints limpios y el dominio agnóstico a HTTP.

---

## 7. Guía de Endpoints de la API

| Verbo  | Ruta              | Descripción                      | Autenticación |
| :----- | :---------------- | :------------------------------- | :------------ |
| `POST` | `/auth/create-user` | Crea un nuevo usuario.           | No            |
| `POST` | `/auth/login`       | Autentica y devuelve un token JWT. | No            |
| `POST` | `/auth/get-user`    | Obtiene un usuario por ID o email. | Requerida     |
| `POST` | `/auth/update-user` | Actualiza un usuario existente.  | Requerida     |

---

## 8. Testing

*(Esta sección se completará más adelante)*

La estrategia de testing debe seguir la misma separación de la arquitectura:
-   **Tests Unitarios:** Para los `UseCases` y `Mappers`. Se mockean las dependencias (como los gateways). Deben residir en `tests/unit/`.
-   **Tests de Integración:** Para los `Adapters` (ej. `Persistence`). Se prueba la integración con servicios reales pero controlados (ej. una base de datos de prueba). Deben residir en `tests/integration/`.
-   **Tests End-to-End:** Para los `EntryPoints`. Se usa un cliente HTTP para probar el flujo completo de la API. Deben residir en `tests/e2e/`.
