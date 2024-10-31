from sqlalchemy import String, Column

from models import BaseModel


class User(BaseModel):
    __tablename__ = 'user'
    username = Column(String)
    name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    phone = Column(String)
    image = Column(String)