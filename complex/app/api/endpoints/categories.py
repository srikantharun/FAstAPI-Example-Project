from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List

from app.api.dependencies.auth import get_current_active_superuser, get_current_user
from app.db.session import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import Category as CategorySchema
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryWithItems

router = APIRouter()


@router.get("/", response_model=List[CategorySchema])
def read_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve categories.
    
    Args:
        db: SQLAlchemy session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of categories
    """
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories


@router.post("/", response_model=CategorySchema)
def create_category(
    *,
    db: Session = Depends(get_db),
    category_in: CategoryCreate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Create new category.
    
    Only superusers can create categories.
    
    Args:
        db: SQLAlchemy session
        category_in: Category data
        current_user: Current authenticated superuser
        
    Returns:
        Created category
        
    Raises:
        HTTPException: If category with this name already exists
    """
    # Check if category with this name already exists
    category = db.query(Category).filter(Category.name == category_in.name).first()
    if category:
        raise HTTPException(
            status_code=400,
            detail="The category with this name already exists",
        )
    
    # Create new category
    category = Category(**category_in.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("/{id}", response_model=CategorySchema)
def read_category(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """
    Get category by ID.
    
    Args:
        db: SQLAlchemy session
        id: Category ID
        
    Returns:
        Category with specified ID
        
    Raises:
        HTTPException: If category not found
    """
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/{id}/items", response_model=CategoryWithItems)
def read_category_with_items(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """
    Get category with all its items.
    
    Args:
        db: SQLAlchemy session
        id: Category ID
        
    Returns:
        Category with its items
        
    Raises:
        HTTPException: If category not found
    """
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{id}", response_model=CategorySchema)
def update_category(
    *,
    db: Session = Depends(get_db),
    id: int,
    category_in: CategoryUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Update a category.
    
    Only superusers can update categories.
    
    Args:
        db: SQLAlchemy session
        id: Category ID
        category_in: Category data to update
        current_user: Current authenticated superuser
        
    Returns:
        Updated category
        
    Raises:
        HTTPException: If category not found
    """
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if updated name conflicts with existing category
    if category_in.name != category.name:
        existing = db.query(Category).filter(Category.name == category_in.name).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="The category with this name already exists",
            )
    
    # Update category fields
    for field, value in category_in.dict().items():
        setattr(category, field, value)
    
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{id}")
def delete_category(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Delete a category.
    
    Only superusers can delete categories.
    
    Args:
        db: SQLAlchemy session
        id: Category ID
        current_user: Current authenticated superuser
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If category not found or has associated items
    """
    category = db.query(Category).filter(Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has items
    if category.items and len(category.items) > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category that has items. Remove all items first.",
        )
    
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}