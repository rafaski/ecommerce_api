from aredis_om import Field, HashModel
from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from datetime import datetime

from ecommerce_api.dependencies.redis_connection import redis_connection
from ecommerce_api.enums import ProductCategory, OrderStatus


class Output(BaseModel):
    """
    user output layout
    """
    success: bool
    message: Optional[str] = None
    results: Optional[Any] = None


class Product(HashModel):
    """
    Product schema
    """
    name: str = Field(index=True, full_text_search=True)
    price: float = Field(index=True)
    quantity: int = Field(ge=0)
    category: ProductCategory = Field(index=True)
    description: Optional[str] = None
    date_posted: str = datetime.today()

    class Meta:
        """
        connecting product class to redis db
        """
        database = redis_connection


class Order(HashModel):
    """
    Order schema
    """
    product_id: str
    quantity: int = Field(ge=1)
    price: float
    status: OrderStatus = Field(index=True, default=OrderStatus.PENDING)

    @property
    def total(self):
        return self.quantity * self.price

    class Meta:
        """
        connecting product class to redis db
        """
        database = redis_connection


class User(BaseModel):
    """
    User schema
    """
    email: EmailStr = Field(default=None, index=True)
    password: str = Field(default=None)
    join_date: str = datetime.today()


# class UserLogin(BaseModel):
#     """
#     User login schema
#     """
#     email: EmailStr = Field(default=None)
#     password: str = Field(default=None)

