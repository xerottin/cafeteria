from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship
from models import BaseModel


class Cafeteria(BaseModel):
    __tablename__ = 'cafeteria'
    name = Column(String, nullable=False)
    phone = Column(String)
    url = Column(String)
    latitude = Column(Float)  # Широта
    longitude = Column(Float)  # Долгота
    rating = Column(Float)
    company_id = Column(Integer, ForeignKey('company.id'))

    menu = relationship("Menu", back_populates="cafeteria")
    company = relationship('Company', back_populates='cafeteria')


class Menu(BaseModel):
    __tablename__ = 'menu'
    item_name = Column(String, nullable=False)
    price = Column(Float)
    description = Column(String)

    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'))
    cafeteria = relationship('Cafeteria', back_populates='menu')


class Coffee(BaseModel):
    __tablename__ = 'coffee'
    name = Column(String, nullable=False)
    origin = Column(String)
    flavor_profile = Column(String)
    bean_type = Column(String)
    price = Column(Float)
    weight = Column(Integer)
    stock = Column(Integer)
    is_available = Column(Boolean, default=True)
    harvest_date = Column(Date)
    rating = Column(Float)
    reviews_count = Column(Integer)
