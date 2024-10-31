from pydantic import BaseModel


class ClientBase(BaseModel):
    id: int
    name: str
    phone: str | None = None
    url: str | None = None
    company_id: str | None = None

class ClientInDB(ClientBase):
    created_at: str
    updated_at: str
    hashed_password: str

class ClientCreate(ClientBase):
    password: str

class ClientUpdate(ClientBase):
    password: str
