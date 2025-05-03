from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.schemas.user import UserCreate
from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.models.category import Category


# Create tables
def init_db(db: Session) -> None:
    """
    Initialize the database with required tables and seed data.
    
    Args:
        db: SQLAlchemy session
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a default admin user if it doesn't exist
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user_in = UserCreate(
            email="admin@example.com",
            password="admin123",
            full_name="Administrator",
            is_superuser=True,
        )
        db_user = User(
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_superuser=user_in.is_superuser,
        )
        db.add(db_user)
        db.commit()
    
    # Create default categories if they don't exist
    categories = ["Electronics", "Books", "Clothing", "Home", "Sports"]
    for category_name in categories:
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            db_category = Category(name=category_name)
            db.add(db_category)
    
    db.commit()