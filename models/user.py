from sqlalchemy import String, Column, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import BaseModel

class User(BaseModel):
    __tablename__ = 'user'
    username = Column(String, unique=True)
    password = Column(String, nullable=False)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    image = Column(String)

    orders = relationship('Order', back_populates="user")

class Order(BaseModel):
    __tablename__ = 'order'
    user_id = Column(Integer, ForeignKey('user.id'))
    status = Column(Boolean, default=True)

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(BaseModel):
    __tablename__ = 'order_item'
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    order_id = Column(Integer, ForeignKey('order.id'))
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
    coffee = relationship("Coffee")
