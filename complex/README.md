# Complex FastAPI Application

This is a full-featured FastAPI application that demonstrates advanced concepts and best practices.

## Features

- Structured project layout with modular components
- SQLAlchemy ORM with SQLite database
- JWT-based authentication and authorization
- Role-based access control (regular users and superusers)
- API versioning and API router
- Advanced Pydantic validation schemas
- Database migrations with Alembic
- HTML templates with Jinja2
- Static file serving
- Advanced search and filtering
- Dependency injection
- Environment-based configuration
- Automatic OpenAPI documentation

## Project Structure

```
complex/
├── app/                 # Main application package
│   ├── api/             # API related code
│   │   ├── dependencies/  # Dependency injection functions
│   │   ├── endpoints/     # API route handlers
│   │   └── api.py         # API router configuration
│   ├── core/            # Core functionality
│   │   ├── config.py      # Application settings
│   │   └── security.py    # Security utilities (JWT, password hashing)
│   ├── db/              # Database related code
│   │   ├── base.py        # SQLAlchemy models
│   │   ├── init_db.py     # Database initialization
│   │   └── session.py     # Database session management
│   ├── models/          # SQLAlchemy models
│   │   ├── user.py        # User model
│   │   ├── item.py        # Item model
│   │   └── category.py    # Category model
│   ├── schemas/         # Pydantic models for request/response
│   │   ├── user.py        # User schemas
│   │   ├── item.py        # Item schemas
│   │   └── category.py    # Category schemas
│   ├── static/          # Static files (CSS, JS, images)
│   └── templates/       # Jinja2 templates for HTML responses
├── main.py              # Main application entry point
└── README.md            # Project documentation
```

## API Flow Diagram

```
┌──────────────┐       ┌───────────┐       ┌───────────────┐       ┌───────────┐
│              │       │           │       │               │       │           │
│    Client    │──────▶│  FastAPI  │──────▶│  API Routers  │──────▶│  Services │
│              │       │    App    │       │               │       │           │
│              │◀──────│           │◀──────│               │◀──────│           │
└──────────────┘       └───────────┘       └───────────────┘       └─────┬─────┘
                            │                      ▲                      │
                            ▼                      │                      ▼
                      ┌───────────┐         ┌──────┴─────┐         ┌───────────┐
                      │           │         │            │         │           │
                      │ Templates │         │ Dependencies│         │ SQLAlchemy│
                      │(Frontend) │         │            │         │    ORM    │
                      │           │         │            │         │           │
                      └───────────┘         └────────────┘         └─────┬─────┘
                                                                         │
                                                                         ▼
                                                                   ┌───────────┐
                                                                   │           │
                                                                   │  SQLite   │
                                                                   │ Database  │
                                                                   │           │
                                                                   └───────────┘
```

## Authentication Flow

```
┌──────────────┐       ┌───────────┐       ┌───────────┐
│              │ 1.Send │           │  2.Verify │           │
│    Client    │──────▶│  /login   │──────────▶│  Database  │
│              │ Credentials      │   User    │           │
│              │◀──────│           │◀──────────│           │
└──────────────┘ 4.Return  └───────────┘  3.Return  └───────────┘
    │  Token                                 User
    │
    │
    ▼
┌──────────────┐       ┌───────────┐       ┌───────────┐
│              │ 5.API  │           │ 6.Validate│           │
│    Client    │──────▶│  API      │──────────▶│  JWT      │
│   + Token    │ Request │  Endpoint  │   Token   │  Validation│
│              │◀──────│           │◀──────────│           │
└──────────────┘ 8.Return └───────────┘  7.Token   └───────────┘
                  Response               Valid/Invalid
```

## API Endpoints

### Authentication
- `POST /api/v1/login/access-token`: Get JWT token

### Users
- `GET /api/v1/users/`: Get all users (superuser only)
- `POST /api/v1/users/`: Create a new user (superuser only)
- `GET /api/v1/users/me`: Get current user info
- `GET /api/v1/users/me/items`: Get current user with items
- `PUT /api/v1/users/me`: Update current user
- `GET /api/v1/users/{user_id}`: Get a specific user (superuser only)

### Items
- `GET /api/v1/items/`: Get all items with filtering
- `POST /api/v1/items/`: Create a new item
- `GET /api/v1/items/{id}`: Get a specific item
- `PUT /api/v1/items/{id}`: Update an item
- `DELETE /api/v1/items/{id}`: Delete an item

### Categories
- `GET /api/v1/categories/`: Get all categories
- `POST /api/v1/categories/`: Create a new category (superuser only)
- `GET /api/v1/categories/{id}`: Get a specific category
- `GET /api/v1/categories/{id}/items`: Get a category with its items
- `PUT /api/v1/categories/{id}`: Update a category (superuser only)
- `DELETE /api/v1/categories/{id}`: Delete a category (superuser only)

## Running the Application

1. Activate the virtual environment:
   ```
   source ../../venv/bin/activate
   ```

2. Install additional dependencies:
   ```
   pip install python-jose passlib python-multipart jinja2 pydantic-settings alembic email-validator
   ```

3. Run the application:
   ```
   python main.py
   ```

4. Access the API at http://localhost:8000
5. Access the documentation at http://localhost:8000/api/v1/docs or http://localhost:8000/api/v1/redoc

Note: The Swagger documentation is available at http://localhost:8000/api/v1/docs (not at the default /docs path)

## Default Credentials

The application is initialized with a default superuser:
- Email: admin@example.com
- Password: admin123