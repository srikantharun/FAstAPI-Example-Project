from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os

# Add the parent directory to sys.path to enable absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from moderate.database import create_tables
from moderate.routers import items

# Initialize FastAPI app
app = FastAPI(
    title="Moderate FastAPI Example",
    description="A more structured API with SQLite database and middlewares",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items.router)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

@app.get("/")
def read_root():
    """Return a welcome message."""
    return {"message": "Welcome to the Moderate FastAPI Example!"}

if __name__ == "__main__":
    uvicorn.run("moderate.main:app", host="0.0.0.0", port=8000, reload=True)