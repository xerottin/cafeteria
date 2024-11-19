from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


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
    url: str
    phone: str
    latitude: float
    longitude: float
    company_id: int


class CafeteriaUpdate(CafeteriaBase):
    username: Optional[str] | None = None
    password: Optional[str] | None = None
    phone: Optional[str] | None = None
    url: Optional[str] | None = None
    latitude: Optional[float] | None = None
    longitude: Optional[float] | None = None
    logo: Optional[str] | None = None
    company_id: Optional[int] | None = None

    @validator("*", pre=True, always=True)
    def ignore_default_string(cls, v):
        return v if v not in (None, "string") else None


class CafeteriaResponse(BaseModel):
    id: int
    username: str
    latitude: float
    longitude: float

class MenuCreate(BaseModel):
    name: str
    cafeteria_id: int

class MenuUpdate(MenuCreate):
    pass


class CoffeeCreate(BaseModel):
    name: str
    origin: str
    flavor_profile: str
    bean_type: str
    weight: int
    stock: int
    price: int
    menu_id: int
    is_available: bool