from sqlalchemy import String, Column

from models import BaseModel


class User(BaseModel):
    __tablename__ = 'user'
    username = Column(String,nullable=False)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)
    image = Column(String)