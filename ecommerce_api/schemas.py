from aredis_om import Field, HashModel
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Any
from datetime import datetime

from ecommerce_api.dependencies.redis_connection import redis_connection
from ecommerce_api.enums import Category, OrderStatus
from ecommerce_api.errors import BadRequest


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
    name: str = Field(index=True,full_text_search=True)
    price: float = Field
    quantity: int = Field
    category: Category = Field(index=True)
    description: Optional[str] = None
    date_posted: datetime = datetime.today()

    @validator("quantity")
    def quantity_validator(cls, value: int):
        if value < 0:
            raise BadRequest()
        return value

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
    quantity: int
    price: float
    total: float
    status: OrderStatus

    class Meta:
        """
        connecting product class to redis db
        """
        database = redis_connection


class User(BaseModel):
    """
    User schema
    """
    fullname: str = Field(default=None, index=True)
    email: EmailStr = Field(default=None, index=True)
    password: str = Field(default=None, index=True)
    join_date: datetime = datetime.today()


class UserLogin(BaseModel):
    """
    User login schema
    """
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

