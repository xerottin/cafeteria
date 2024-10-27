from datetime import datetime

from models import BaseModel


class AdminBase(BaseModel):
    username: str
    password: str

class AdminInDB(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime


class AdminCreate(AdminBase):
    pass
