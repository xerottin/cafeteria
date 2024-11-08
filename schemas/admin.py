from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Literal


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str | None = None
    client_id: str | None = None
    user_type: Literal["admin", "cafeteria"]
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