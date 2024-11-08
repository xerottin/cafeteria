from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserInDB(BaseModel):
    id: int
    username: str
    access_token: str
    token_type: str = "bearer"


class User(UserBase):
    id: int
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    image: Optional[str] = None


class CurrentUserScheme(UserUpdate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]