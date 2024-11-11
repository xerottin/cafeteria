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
    password: Optional[str] | None = None
    phone: Optional[str] | None = None
    email: Optional[str] | None = None
    owner: Optional[str] | None = None

