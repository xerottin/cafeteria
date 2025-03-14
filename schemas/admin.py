from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str | None = None
    user_type: Literal["admin", "cafeteria", "user"]


class AdminBase(BaseModel):
    username: str
    password: str


class AdminCreate(AdminBase):
    pass


class AdminResponse(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime


class AdminUpdate(AdminBase):
    pass


class AdminInDB(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime
