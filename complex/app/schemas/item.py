from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Shared properties
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)


# Properties to receive via API on creation
class ItemCreate(ItemBase):
    category_id: int


# Properties to receive via API on update
class ItemUpdate(ItemBase):
    name: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    owner_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties stored in DB but not returned by API
class ItemInDB(ItemInDBBase):
    pass