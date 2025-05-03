from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency for database session.
    
    Yields:
        SQLAlchemy session
    
    This function is used with FastAPI's dependency injection system
    to provide a database session to route handlers.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()