from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Company(BaseModel):
    __tablename__ = 'company'
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    owner = Column(String)
    hashed_password = Column(String)

    clients = relationship('Client', back_populates='company')
