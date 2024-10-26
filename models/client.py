
from sqlalchemy import Column, String

from models import BaseModel


class Client(BaseModel):
    __tablename__ = 'client'
    name = Column(String, primary_key=True)
    phone = Column(String)
    url = Column(String)
