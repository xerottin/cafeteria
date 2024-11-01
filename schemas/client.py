from datetime import datetime

from pydantic import BaseModel


class ClientBase(BaseModel):
    username: str
    password: str


class ClientInDB(ClientBase):
    id: int
    phone: str
    url: str
    company_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    logo: str

class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    username: str | None = None
    password: str | None = None
    phone: str | None = None
    url: str | None = None
    logo: str | None = None
    company_id: int | None = None

