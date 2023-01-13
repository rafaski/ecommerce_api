from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, ForeignKey, DateTime
)

from ecommerce_api.sql.database import Base
from ecommerce_api.auth.hashing import hashing_password, verify_password
from ecommerce_api.enums import OrderStatus


class User(Base):
    """
    User sql table schema
    """
    __tablename__ = "users"

    name = Column(String)
    email = Column(String, unique=True, index=True, primary_key=True)
    password = Column(String)
    order = relationship("Order", back_populates="user_info")
    cart = relationship("Cart", back_populates="user_cart")

    def __init__(self, name, email, password, *args, **kwargs):
        self.name = name
        self.email = email
        self.password = hashing_password(password)

    def check_password(self, password) -> bool:
        verified = verify_password(
            password=self.password,
            hashed_password=password
        )
        return verified


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
    date_posted = Column(String)
    cart_items = relationship("CartItems", back_populates="products")
    order_details = relationship(
        "OrderDetails",
        back_populates="product_order_details"
    )


class Cart(Base):
    """
    Shopping cart sql table schema
    """
    __tablename__ = "cart"

    id = Column(String, primary_key=True)
    user_email = Column(String, ForeignKey(User.email, ondelete="CASCADE"))
    cart_items = relationship("CartItems", back_populates="cart")
    user_cart = relationship("User", back_populates="cart")
    created_date = Column(DateTime, default=datetime.now)


class CartItems(Base):
    """
    Sql table schema for products in shopping cart
    """
    __tablename__ = "cart_items"

    id = Column(String, primary_key=True)
    cart_id = Column(String, ForeignKey(Cart.id, ondelete="CASCADE"))
    product_id = Column(String, ForeignKey(Product.id, ondelete="CASCADE"))
    cart = relationship("Cart", back_populates="cart_items")
    products = relationship("Product", back_populates="cart_items")
    created_date = Column(DateTime, default=datetime.now)


class Order(Base):
    """
    Order sql table schema
    """
    __tablename__ = "order"

    id = Column(String, primary_key=True)
    order_date = Column(DateTime, default=datetime.now)
    order_total = Column(Float, default=0.0)
    order_status = Column(String, default=OrderStatus.PENDING)
    customer_email = Column(String, ForeignKey(User.email, ondelete="CASCADE"))
    order_details = relationship("OrderDetails", back_populates="order")
    user_info = relationship("User", back_populates="order")


class OrderDetails(Base):
    """
    OrderDetails sql table schema
    """
    __tablename__ = "order_details"

    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey(Order.id, ondelete="CASCADE"))
    product_id = Column(String, ForeignKey(Product.id, ondelete="CASCADE"))
    order = relationship("Order", back_populates="order_details")
    product_order_details = relationship(
        "Product",
        back_populates="order_details"
    )
    quantity = Column(Integer, default=1)
    created = Column(DateTime, default=datetime.now)
