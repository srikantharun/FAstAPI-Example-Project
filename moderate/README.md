# Moderate FastAPI Application

This is a more structured API with SQLite database and middlewares that demonstrates intermediate concepts of FastAPI.

## Features

- Structured project layout with modular components
- SQLAlchemy ORM with SQLite database
- API routers for better organization
- Request/response models with Pydantic validation
- Query parameters and filtering
- CORS middleware
- Automatic OpenAPI documentation

## Project Structure

```
moderate/
├── __init__.py         # Package initialization
├── database.py         # Database configuration and models
├── main.py             # Main application entry point
├── models.py           # Pydantic models for request/response
├── routers/
│   ├── __init__.py     # Router package initialization
│   └── items.py        # Item router with CRUD operations
└── README.md           # Documentation
```

## API Flow Diagram

```
┌──────────────┐       ┌───────────┐       ┌───────────┐       ┌───────────┐
│              │       │           │       │           │       │           │
│    Client    │──────▶│  FastAPI  │──────▶│  Routers  │──────▶│  SQLite   │
│              │       │    App    │       │           │       │ Database  │
│              │◀──────│           │◀──────│           │◀──────│           │
└──────────────┘       └───────────┘       └───────────┘       └───────────┘
                           │  ▲
                           │  │
                           ▼  │
                       ┌───────────┐
                       │           │
                       │ Middleware│
                       │           │
                       └───────────┘
```

## API Endpoints

- `GET /`: Welcome message
- `GET /items`: Get all items with filtering and pagination
- `GET /items/{item_id}`: Get a specific item
- `POST /items`: Create a new item
- `PUT /items/{item_id}`: Update an existing item
- `DELETE /items/{item_id}`: Delete an item

## Running the Application

1. Activate the virtual environment:
   ```
   source ../../venv/bin/activate
   ```

2. Run the application:
   ```
   python -m moderate.main
   ```

3. Access the API at http://localhost:8000
4. Access the documentation at http://localhost:8000/docs or http://localhost:8000/redoc