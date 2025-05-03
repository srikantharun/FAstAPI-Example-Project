from pydantic import BaseModel
from typing import Optional, List

from app.schemas.item import Item


# Shared properties
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


# Properties to receive via API on creation
class CategoryCreate(CategoryBase):
    pass


# Properties to receive via API on update
class CategoryUpdate(CategoryBase):
    pass


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    pass


# Properties to return to client with items
class CategoryWithItems(CategoryInDBBase):
    items: List[Item] = []