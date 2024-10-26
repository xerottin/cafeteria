from sqlalchemy import Column, String

from models.base import BaseModel


class Company(BaseModel):
    __tablename__ = 'company'
    name = Column(String, primary_key=True)
    phone = Column(String)
    email = Column(String)
    owner = Column(String)