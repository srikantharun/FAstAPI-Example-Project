from pydantic_settings import BaseSettings
from typing import List, Optional
import secrets
from functools import lru_cache


class Settings(BaseSettings):
    # Base settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Complex FastAPI Example"
    PROJECT_DESCRIPTION: str = "A complex REST API with advanced features"
    PROJECT_VERSION: str = "1.0.0"
    
    # Security settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Database settings
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./complex_app.db"
    
    # Email settings (for a production app, these would be used)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """
    Returns application settings as a singleton.
    
    Uses lru_cache for performance, so the settings are computed once
    and reused for all subsequent calls.
    """
    return Settings()