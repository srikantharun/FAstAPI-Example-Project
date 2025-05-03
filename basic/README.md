# Basic FastAPI Application

This is a simple REST API with in-memory storage that demonstrates the fundamental concepts of FastAPI.

## Features

- Basic CRUD operations for a simple Item model
- Input validation with Pydantic
- Error handling with HTTPExceptions
- Automatic OpenAPI documentation

## Project Structure

```
basic/
├── main.py     # The FastAPI application
└── README.md   # Documentation
```

## API Flow Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│              │       │              │       │              │
│    Client    │──────▶│  FastAPI App │──────▶│  In-Memory   │
│              │       │              │       │   Database   │
│              │◀──────│              │◀──────│              │
└──────────────┘       └──────────────┘       └──────────────┘
```

## API Endpoints

- `GET /`: Welcome message
- `GET /items`: Get all items
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
   python main.py
   ```

3. Access the API at http://localhost:8000
4. Access the documentation at http://localhost:8000/docs or http://localhost:8000/redoc