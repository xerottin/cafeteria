from datetime import datetime

from pydantic import BaseModel

class AdminBase(BaseModel):
    username: str
    password: str


class AdminInDB(AdminBase):
    created_at: datetime
    updated_at: datetime
    hashed_password: str


class AdminCreate(AdminBase):
    pass

