from datetime import datetime

from pydantic import BaseModel


class CafeteriaBase(BaseModel):
    username: str
    password: str


class CafeteriaInDB(CafeteriaBase):
    id: int
    phone: str
    url: str
    company_id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    logo: str

class CafeteriaCreate(CafeteriaBase):
    pass


class CafeteriaUpdate(CafeteriaBase):
    username: str | None = None
    password: str | None = None
    phone: str | None = None
    url: str | None = None
    latitude: str | None = None
    longitude: str | None = None
    logo: str | None = None
    company_id: int | None = None

class CafeteriaResponse(BaseModel):
    id: int
    username: str
    latitude: float
    longitude: float