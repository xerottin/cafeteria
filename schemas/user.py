from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserInDB(BaseModel):
    id: int
    username: str
    password: str
    name: str
    email: str
    phone: str
    image: str

class User(UserBase):
    id: int
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    username: Optional[str] | None = None
    name: Optional[str] | None = None
    password: Optional[str] = None
    email: Optional[str]  | None = None
    phone: Optional[str]  | None = None
    image: Optional[str]  | None = None


class CurrentUserScheme(UserUpdate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class OrderItem(BaseModel):
    coffee_id: int
    quantity: int

class OrderCreate(BaseModel):
    cafeteria_id: int
    user_id: int
    status: bool
    order_items: List[OrderItem]

class OrderInDB(BaseModel):
    cafeteria_id: int
    user_id: int
    status: bool