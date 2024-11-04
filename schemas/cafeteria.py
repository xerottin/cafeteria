from datetime import datetime
from typing import Optional

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
    username: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    logo: Optional[str] = None
    company_id: Optional[int] = None

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