from pydantic import BaseModel, EmailStr
from typing import Optional, List

from app.schemas.item import Item


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties to return to client with items
class UserWithItems(UserInDBBase):
    items: List[Item] = []


# Properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    hashed_password: str