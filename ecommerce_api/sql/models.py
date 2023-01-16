from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, String, Text, Float, ForeignKey, DateTime
)
from datetime import datetime

from ecommerce_api.sql.database import Base
from ecommerce_api.enums import OrderStatus


class User(Base):
    """
    User sql table schema
    """
    __tablename__ = "user"

    email = Column(String, unique=True, index=True, primary_key=True)
    password = Column(String)
    type = Column(String)
    orders = relationship("Order", backref="user", lazy='subquery')


class Product(Base):
    """
    Product sql table schema
    """
    __tablename__ = "product"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    category = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    order_id = Column(String, ForeignKey("order.id", ondelete="CASCADE"))


class Order(Base):
    """
    Order sql table schema
    """
    __tablename__ = "order"

    id = Column(String, primary_key=True)
    created_date = Column(String)
    total_price = Column(Float)
    status = Column(String)
    user_email = Column(String, ForeignKey("user.email", ondelete="CASCADE"))
    products = relationship("Product", backref="order", lazy='subquery')

