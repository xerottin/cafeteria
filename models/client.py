
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models import BaseModel


class Client(BaseModel):
    __tablename__ = 'client'
    username = Column(String, nullable=False)
    phone = Column(String)
    url = Column(String)
    hashed_password = Column(String)
    company_id = Column(Integer, ForeignKey('company.id'))

    company = relationship('Company', back_populates='clients')
