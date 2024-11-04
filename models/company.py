from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Company(BaseModel):
    __tablename__ = 'company'
    username = Column(String, nullable=False, unique=True)
    password = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    owner = Column(String)
    logo = Column(String)

    cafeterias = relationship('Cafeteria', back_populates='company')
