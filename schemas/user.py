from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserInDB(BaseModel):
    id: int
    username: str
    access_token: str
    token_type: str = "bearer"


class User(UserBase):
    id: int
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    id: int
    password: str | None = None
    email: str | None = None
    phone: str | None = None
    image: str | None = None