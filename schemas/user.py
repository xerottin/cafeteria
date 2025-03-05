from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, validator


class UserBase(BaseModel):
    username: str

class UserInDB(BaseModel):
    id: int
    username: str
    name: str
    password: str
    email: str
    phone: str
    image: str

class UserCreate(UserBase):
    name: str
    password: str
    email: str
    phone: str
    image: str

class UserUpdate(BaseModel):
    username: Optional[str] | None = None
    name: Optional[str] | None = None
    password: Optional[str] = None
    email: Optional[str]  | None = None
    phone: Optional[str]  | None = None
    image: Optional[str]  | None = None

    @validator("*", pre=True, always=True)
    def ignore_default_string(cls, v):
        return v if v not in (None, "string") else None

class CurrentUserScheme(UserUpdate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class OrderItem(BaseModel):
    coffee_id: int
    quantity: int

class OrderCreate(BaseModel):
    cafeteria_id: int
    status: bool
    order_items: List[OrderItem]

class OrderInDB(BaseModel):
    cafeteria_id: int
    user_id: int
    status: bool


class FavoriteSchemas(BaseModel):
    user_id: int
    coffee_id: int
