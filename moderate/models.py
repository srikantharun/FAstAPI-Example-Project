from pydantic import BaseModel, Field
from typing import Optional, List

# Request Models
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    category: str

class ItemCreate(ItemBase):
    pass

# Response Models
class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True

class ItemList(BaseModel):
    items: List[Item]
    total: int

class MessageResponse(BaseModel):
    message: str