from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from models import BaseModel

class Cafeteria(BaseModel):
    __tablename__ = 'cafeteria'
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String)
    url = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float)
    company_id = Column(Integer, ForeignKey('company.id'))

    orders = relationship('Order', back_populates='cafeteria')
    menu = relationship("Menu", back_populates="cafeteria")
    company = relationship('Company', back_populates='cafeterias')


class Menu(BaseModel):
    __tablename__ = 'menu'
    name = Column(String, nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'))

    cafeteria = relationship('Cafeteria', back_populates='menu')
    coffees = relationship('Coffee', back_populates='menu')


class Coffee(BaseModel):
    __tablename__ = 'coffee'
    name = Column(String, nullable=False)
    origin = Column(String)
    flavor_profile = Column(String)
    bean_type = Column(String)
    price = Column(Integer)
    weight = Column(Integer)
    stock = Column(Integer)
    is_available = Column(Boolean, default=True)
    rating = Column(Float, default=0.0)
    menu_id = Column(Integer, ForeignKey('menu.id'))

    menu = relationship("Menu", back_populates="coffees")
    favorites = relationship("Favorite", back_populates="coffee")

