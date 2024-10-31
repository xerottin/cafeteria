from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    username: str

class UserInDB(BaseModel):
    username: str
    access_token: str
    token_type: str = "bearer"


class User(UserBase):
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str | None = None
    email: str | None = None
    phone: str | None = None
    image: str | None = None