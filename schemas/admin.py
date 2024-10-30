from datetime import datetime

from models import BaseModel


class AdminBase(BaseModel):
    id: int
    name: str

class AdminInDB(AdminBase):
    created_at: datetime
    updated_at: datetime
    hashed_password: str


class AdminCreate(AdminBase):
    password: str


