from typing import Optional

from pydantic import BaseModel


class CompanyBase(BaseModel):
    username: str

class CompanyInDB(CompanyBase):
    id: int
    phone: str
    email: str
    owner: str
    hashed_password: str

class CompanyCreate(CompanyBase):
    password: str
    phone: str
    email: str
    owner: str

class CompanyUpdate(CompanyBase):
    password: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    owner: Optional[str] = None

