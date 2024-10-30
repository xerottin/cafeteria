from datetime import datetime
from pydantic import BaseModel

class UserInDB(BaseModel):
    username: str
    access_token: str
    token_type: str = "bearer"


class User(BaseModel):
    username: str
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    password: str
