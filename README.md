# Arquetipo de Backend con FastAPI y Arquitectura Hexagonal

![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![Arquitectura](https://img.shields.io/badge/Arquitectura-Hexagonal-purple.svg)

API RESTful asíncrona construida con Python y FastAPI, siguiendo los principios de la Arquitectura Hexagonal (Puertos y Adaptadores) para lograr un alto desacoplamiento y mantenibilidad.

---

## Tabla de Contenidos

1.  [Sobre el Proyecto](#sobre-el-proyecto)
2.  [Primeros Pasos](#primeros-pasos)
    *   [Prerrequisitos](#prerrequisitos)
    *   [Instalación](#instalación)
3.  [Ejecutar la Aplicación](#ejecutar-la-aplicación)
4.  [Estructura del Proyecto](#estructura-del-proyecto)
5.  [Conceptos Arquitectónicos Clave](#conceptos-arquitectónicos-clave)
    *   [Manejo de Excepciones](#manejo-de-excepciones)
    *   [Inyección de Dependencias](#inyección-de-dependencias)
    *   [Configuración](#configuración)
6.  [Guía de Endpoints de la API](#guía-de-endpoints-de-la-api)
7.  [Testing](#testing)

---

## Sobre el Proyecto

Este proyecto sirve como un arquetipo de nivel profesional para construir servicios de backend robustos, testeables y escalables. Se basa en los siguientes pilares:

-   **Framework Asíncrono:** Utiliza **FastAPI** para obtener un alto rendimiento en operaciones de I/O intensivas.
-   **Arquitectura Hexagonal:** Separa estrictamente la **lógica de negocio (dominio)** de los detalles de **infraestructura** (framework web, base de datos). Esto permite que el núcleo de la aplicación sea independiente de la tecnología externa.
-   **Código Limpio y Desacoplado:** Aplica principios como la Inversión de Dependencias (a través de gateways/interfaces) y el Patrón Repositorio para una clara separación de responsabilidades.

---

## Primeros Pasos

### Prerrequisitos

-   Python 3.11 o superior
-   Poetry (recomendado) o `pip` para la gestión de dependencias
-   Una instancia de PostgreSQL en ejecución
-   Docker (opcional, para ejecutar la base de datos)

### Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone https://[URL-DEL-REPOSITORIO]
    cd [NOMBRE-DEL-DIRECTORIO]
    ```

2.  **Crea un entorno virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura las variables de entorno:**
    Crea un archivo `.env` a partir del ejemplo `.env.example` y rellena los valores, especialmente los de la conexión a la base de datos.
    ```bash
    cp .env.example .env
    # Edita el archivo .env con tus configuraciones
    ```

---

## Ejecutar la Aplicación

Para iniciar el servidor de desarrollo, ejecuta:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.

---

## Estructura del Proyecto

*(Esta sección se completará más adelante)*

---

## Conceptos Arquitectónicos Clave

### Manejo de Excepciones

El proyecto utiliza un patrón de **Manejo Centralizado de Excepciones Basado en Tipos** para asegurar un código limpio, desacoplado y predecible.

#### Filosofía

1.  **El Dominio Lanza Excepciones Semánticas:** El código de negocio (`domain`, `usecase`) no sabe nada de HTTP. Lanza excepciones con nombres claros que describen el problema de negocio (ej. `UserNotFoundException`).
2.  **Los Endpoints son Limpios:** La capa de la API (`entry_point`) no contiene bloques `try/except`. Su única función es llamar a los casos de uso y devolver resultados exitosos.
3.  **Una Capa Centralizada Traduce Errores:** Un conjunto de "manejadores de excepciones", registrados en la instancia de FastAPI, captura estas excepciones de dominio y las traduce a respuestas HTTP estandarizadas (404, 409, 401, etc.).

#### Flujo de una Excepción

El flujo sigue un patrón de "Nacimiento -> Burbujeo -> Traducción":

1.  **Nacimiento:** La excepción nace en la capa más profunda que tiene el contexto para entender el error. Por ejemplo, la capa de persistencia convierte un `IntegrityError` de la base de datos en un `DuplicateUserException`.
2.  **Burbujeo:** La excepción de dominio viaja hacia arriba a través de las capas (persistencia -> caso de uso -> endpoint) sin ser capturada.
3.  **Traducción:** Justo antes de que la aplicación se rompa, el manejador global correspondiente la intercepta y la convierte en una `JSONResponse` con el código de estado y mensaje correctos.

#### Cómo Añadir una Nueva Excepción (Ejemplo)

Supongamos que queremos evitar que se cree un usuario con un `profile_id` que no existe.

**Paso 1: Definir la Excepción Semántica**

En `app/domain/model/util/exceptions.py`, añade una nueva clase de excepción:

```python
class ProfileNotFoundException(DomainException):
    """Lanzada cuando se intenta usar un profile_id que no existe."""
    def __init__(self, profile_id: int):
        message = f"El perfil con ID '{profile_id}' no existe."
        super().__init__(message)
```

**Paso 2: Lanzar la Excepción donde Nace**

El lugar correcto es el adaptador de persistencia, que puede interpretar el error de clave foránea de la base de datos.

En `app/infrastructure/driven_adapter/persistence/service/persistence.py`, modifica el método `create_user`:

```python
# Dentro del método create_user
except IntegrityError as e:
    await self.session.rollback()
    # Asumiendo que el nombre de la constraint de FK es 'fk_users_profile_id'
    if "fk_users_profile_id" in str(e.orig):
        raise ProfileNotFoundException(profile_id=user.profile_id)
    else:
        raise DuplicateUserException(email=user.email)
```

**Paso 3: Crear el Manejador de la Excepción**

En `app/infrastructure/entry_point/utils/exception_handler.py`, añade una nueva función manejadora que traducirá la excepción a una respuesta HTTP. Un error de este tipo suele corresponder a un `400 Bad Request`.

```python
from app.domain.model.util.exceptions import ProfileNotFoundException

async def profile_not_found_exception_handler(request: Request, exc: ProfileNotFoundException):
    """Manejador para ProfileNotFoundException (HTTP 400)."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )
```

**Paso 4: Registrar el Nuevo Manejador**

Finalmente, informa a FastAPI sobre este nuevo manejador en `app/application/fast_api.py`. **El orden es importante**: regístralo antes de los manejadores más genéricos.

```python
# ... (importaciones)
from app.domain.model.util.exceptions import ProfileNotFoundException
from app.infrastructure.entry_point.utils.exception_handler import profile_not_found_exception_handler

def create_app() -> FastAPI:
    # ...
    # Registrar manejadores (de más específico a más genérico)
    app.add_exception_handler(ProfileNotFoundException, profile_not_found_exception_handler)
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    # ... resto de manejadores
    return app
```

Con estos cuatro pasos, has integrado un nuevo flujo de error de forma limpia y mantenible en toda la aplicación.

### Inyección de Dependencias

*(Esta sección se completará más adelante)*

### Configuración

*(Esta sección se completará más adelante)*

---

## Guía de Endpoints de la API

*(Esta sección se completará más adelante)*

---

## Testing

*(Esta sección se completará más adelante)*