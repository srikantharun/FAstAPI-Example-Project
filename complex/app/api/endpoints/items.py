from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.item import Item
from app.models.user import User
from app.schemas.item import Item as ItemSchema
from app.schemas.item import ItemCreate, ItemUpdate

router = APIRouter()


@router.get("/", response_model=List[ItemSchema])
def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    search: Optional[str] = None,
) -> Any:
    """
    Retrieve items with filtering and pagination.
    
    Args:
        db: SQLAlchemy session
        skip: Number of records to skip
        limit: Maximum number of records to return
        category_id: Filter by category ID
        min_price: Filter by minimum price
        max_price: Filter by maximum price
        search: Search in name and description
        
    Returns:
        List of items matching the filters
    """
    # Start with base query
    query = db.query(Item)
    
    # Apply filters
    if category_id is not None:
        query = query.filter(Item.category_id == category_id)
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    if max_price is not None:
        query = query.filter(Item.price <= max_price)
    if search is not None:
        query = query.filter(
            (Item.name.ilike(f"%{search}%")) | 
            (Item.description.ilike(f"%{search}%"))
        )
    
    # Apply pagination
    items = query.offset(skip).limit(limit).all()
    return items


@router.post("/", response_model=ItemSchema)
def create_item(
    *,
    db: Session = Depends(get_db),
    item_in: ItemCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new item.
    
    Args:
        db: SQLAlchemy session
        item_in: Item data
        current_user: Current authenticated user
        
    Returns:
        Created item
    """
    item = Item(
        **item_in.dict(),
        owner_id=current_user.id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{id}", response_model=ItemSchema)
def read_item(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    """
    Get item by ID.
    
    Args:
        db: SQLAlchemy session
        id: Item ID
        
    Returns:
        Item with specified ID
        
    Raises:
        HTTPException: If item not found
    """
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{id}", response_model=ItemSchema)
def update_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    item_in: ItemUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update an item.
    
    Args:
        db: SQLAlchemy session
        id: Item ID
        item_in: Item data to update
        current_user: Current authenticated user
        
    Returns:
        Updated item
        
    Raises:
        HTTPException: If item not found or not owned by current user
    """
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Update item fields
    update_data = item_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{id}")
def delete_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete an item.
    
    Args:
        db: SQLAlchemy session
        id: Item ID
        current_user: Current authenticated user
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If item not found or not owned by current user
    """
    item = db.query(Item).filter(Item.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}