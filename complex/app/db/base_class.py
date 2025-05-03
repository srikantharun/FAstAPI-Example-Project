from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    Base class for SQLAlchemy models.
    
    Provides automatic table name generation and common functionalities.
    """
    id: Any
    __name__: str
    
    # Generate __tablename__ automatically based on class name
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name from the class name.
        
        Transforms CamelCase to snake_case (e.g., UserModel becomes user_model).
        """
        return cls.__name__.lower()