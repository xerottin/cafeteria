from sqlalchemy import String, Column, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import BaseModel


class User(BaseModel):
    __tablename__ = 'user'
    username = Column(String, unique=True)
    name = Column(String)
    password = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String)
    image = Column(String)

    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)

    orders = relationship('Order', back_populates="user")
    favorites = relationship("Favorite", back_populates="user")


class Order(BaseModel):
    __tablename__ = 'order'
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    status = Column(Boolean, default=True)

    cafeteria = relationship('Cafeteria', back_populates='orders')
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(BaseModel):
    __tablename__ = 'order_item'
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    order_id = Column(Integer, ForeignKey('order.id'))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    coffee = relationship("Coffee")


class Favorite(BaseModel):
    __tablename__ = 'favorite'
    user_id = Column(Integer, ForeignKey('user.id'))
    coffee_id = Column(Integer, ForeignKey('coffee.id'))

    user = relationship("User", back_populates="favorites")
    coffee = relationship("Coffee", back_populates="favorites")
