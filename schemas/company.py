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
    password: str | None = None
    phone: str | None = None
    email: str | None = None
    owner: str | None = None

