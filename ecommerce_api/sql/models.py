from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, ForeignKey, DateTime
)

from ecommerce_api.sql.database import Base
from ecommerce_api.enums import OrderStatus, UserType
from ecommerce_api.auth.password import to_hash


class User(Base):
    """
    User sql table schema
    """
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, primary_key=True)
    password = Column(String)
    type = Column(String, default=UserType.CUSTOMER)
    orders = relationship("Order", back_populates="user")

    def __init__(self, password: str, **data):
        self.password = to_hash(password=password)


class Product(Base):
    """
    Product sql table schema
    """
    __tablename__ = "products"

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
    created_date = Column(DateTime, default=datetime.now)
    total_price = Column(Float, default=0.0)
    status = Column(String, default=OrderStatus.IN_PROGRESS)
    user_email = Column(String, ForeignKey("user.email", ondelete="CASCADE"))
    products = relationship("Product", back_populates="order")
    user = relationship("User", back_populates="order")

