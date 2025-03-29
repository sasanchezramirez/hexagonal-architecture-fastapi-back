# Arquitectura Hexagonal con FastAPI

Este proyecto implementa una arquitectura hexagonal (también conocida como puertos y adaptadores) utilizando FastAPI como framework web. La arquitectura está diseñada para ser mantenible, escalable y fácil de probar.

## 🏗️ Arquitectura

El proyecto sigue los principios de la arquitectura hexagonal, dividiendo la aplicación en tres capas principales:

### 1. Dominio (Domain)
- **Modelos**: Entidades y objetos de valor que representan el núcleo del negocio
- **Casos de Uso**: Lógica de negocio principal
- **Puertos**: Interfaces que definen las interacciones con el exterior

### 2. Aplicación (Application)
- **Adaptadores Primarios**: Manejan las entradas (HTTP, CLI, etc.)
- **Adaptadores Secundarios**: Manejan las salidas (base de datos, servicios externos, etc.)

### 3. Infraestructura (Infrastructure)
- Implementaciones concretas de los puertos
- Configuración y conexiones externas

## 🚀 Características

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para manejo de base de datos
- **Pydantic**: Validación de datos y serialización
- **JWT**: Autenticación y autorización
- **Docker**: Contenedorización de la aplicación
- **Arquitectura Hexagonal**: Separación clara de responsabilidades

## 📋 Prerrequisitos

- Python 3.8+
- Docker y Docker Compose
- PostgreSQL (si se ejecuta localmente)

## 🛠️ Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/hexagonal-architecture-fastapi-back.git
cd hexagonal-architecture-fastapi-back
```

2. Construir y ejecutar con Docker:
```bash
docker-compose build --no-cache
docker-compose up
```

3. Acceder a la documentación de la API:
```
http://localhost:8000/docs
```

## 🔧 Configuración

El proyecto utiliza variables de entorno para la configuración. Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
JWT_SECRET_KEY=tu_clave_secreta
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📚 Endpoints

### Autenticación
- `POST /auth/login`: Iniciar sesión
- `POST /auth/create-user`: Crear nuevo usuario
- `GET /auth/get-user`: Obtener usuario por ID o email
- `PUT /auth/update-user`: Actualizar usuario existente

### Usuarios
- `GET /users/{user_id}`: Obtener usuario por ID
- `GET /users/email/{email}`: Obtener usuario por email
- `PUT /users/{user_id}`: Actualizar usuario

## 🧪 Testing

Para ejecutar las pruebas:

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar pruebas
pytest
```

## 📦 Estructura del Proyecto

```
app/
├── domain/
│   ├── model/
│   │   ├── user.py
│   │   └── util/
│   ├── usecase/
│   │   └── user_usecase.py
│   └── gateway/
│       └── persistence_gateway.py
├── infrastructure/
│   ├── entry_point/
│   │   ├── api/
│   │   ├── dto/
│   │   └── mapper/
│   └── driven_adapter/
│       └── persistence/
└── main.py
```

## 🔒 Seguridad

- Autenticación basada en JWT
- Contraseñas hasheadas con bcrypt
- Validación de datos con Pydantic
- Manejo seguro de errores

## 📝 Convenciones de Código

- PEP 8 para estilo de código
- Docstrings en todas las funciones y clases
- Tipado estático con type hints
- Nombres descriptivos para variables y funciones

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **Tu Nombre** - *Trabajo Inicial* - [TuUsuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- FastAPI
- SQLAlchemy
- Pydantic
- Docker
- Y todos los demás proyectos open source que hacen esto posible
