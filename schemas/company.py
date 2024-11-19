from typing import Optional

from pydantic import BaseModel, validator


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
    logo: str
    owner: str

class CompanyUpdate(BaseModel):
    username: Optional[str] | None = None
    password: Optional[str] | None = None
    phone: Optional[str] | None = None
    email: Optional[str] | None = None
    owner: Optional[str] | None = None
    logo: Optional[str] | None = None

    @validator("*", pre=True, always=True)
    def ignore_default_string(cls, v):
        return v if v not in (None, "string") else None