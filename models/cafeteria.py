from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship
from models import BaseModel

class Cafeteria(BaseModel):
    __tablename__ = 'cafeteria'
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
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
    product = Column(String, nullable=False)
    origin = Column(String)
    flavor_profile = Column(String) #вкус
    bean_type = Column(String) # вид кофе
    stock = Column(Integer) #количество
    price = Column(Integer)
    rating = Column(Float)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'))

    cafeteria = relationship('Cafeteria', back_populates='menu')
