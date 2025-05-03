# FastAPI Example Project

This project demonstrates FastAPI implementations at different complexity levels, from basic to complex.

## Project Structure

```
FAstAPI-Example-Project/
├── venv/                # Python virtual environment
├── basic/               # Basic FastAPI implementation
│   ├── main.py          # Simple application with in-memory storage
│   └── README.md        # Documentation
│
├── moderate/            # Moderate FastAPI implementation
│   ├── database.py      # Database configuration
│   ├── main.py          # Application with SQLite and routers
│   ├── models.py        # Pydantic models
│   ├── routers/         # API routers
│   └── README.md        # Documentation
│
└── complex/             # Complex FastAPI implementation
    ├── app/             # Main application package
    │   ├── api/         # API related code
    │   ├── core/        # Core functionality
    │   ├── db/          # Database related code
    │   ├── models/      # SQLAlchemy models
    │   ├── schemas/     # Pydantic models
    │   ├── static/      # Static files
    │   └── templates/   # HTML templates
    ├── main.py          # Application entry point
    └── README.md        # Documentation
```

## Progression of Concepts

1. **Basic**: Simple REST API with in-memory storage
   - Focus on basic FastAPI concepts, routes, and Pydantic models
   - Single file structure with minimal components

2. **Moderate**: More structured API with SQLite database
   - Introduces SQLAlchemy ORM
   - Modular structure with routers
   - Advanced queries and filtering
   - CORS middleware

3. **Complex**: Full-featured application with best practices
   - Advanced project structure
   - Authentication and authorization with JWT
   - Role-based access control
   - HTML templates and static files
   - Advanced dependency injection
   - Environment-based configuration

## Learning Path

This project provides a progressive learning path for FastAPI:

1. Start with the basic implementation to understand core FastAPI concepts
2. Move to the moderate implementation to learn about database integration and project structure
3. Explore the complex implementation to see best practices for real-world applications

## Getting Started

1. Clone the repository:
   ```
   git clone <repository-url>
   cd FAstAPI-Example-Project
   ```

2. Create a virtual environment and install dependencies:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn pydantic python-multipart jinja2 sqlalchemy matplotlib
   pip install python-jose passlib email-validator pydantic-settings  # For complex application
   ```

3. Run any of the three implementations:

   - Basic:
     ```
     cd basic
     python main.py
     ```

   - Moderate:
     ```
     cd moderate
     python -m moderate.main
     ```

   - Complex:
     ```
     cd complex
     python main.py
     ```

4. Access the API documentation at `http://localhost:8000/docs` or `http://localhost:8000/redoc`

## Overall Project Flow Diagram

```
┌──────────────┐
│              │
│    Basic     │  - Simple API with in-memory storage
│              │  - Single file structure
└──────────────┘
        ▼
┌──────────────┐
│              │
│   Moderate   │  - SQLAlchemy ORM with SQLite
│              │  - Modular structure with routers
└──────────────┘
        ▼
┌──────────────┐
│              │
│   Complex    │  - Advanced project structure
│              │  - Authentication & authorization
└──────────────┘  - Multiple database models
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Additional packages depending on the implementation level

Each implementation has its own README with detailed documentation.