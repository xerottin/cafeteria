from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AdminBase(BaseModel):
    username: str

class AdminCreate(AdminBase):
    password: str

class AdminResponse(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime

class AdminUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class AdminInDB(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime