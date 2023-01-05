from redis_om import HashModel
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Any
from datetime import datetime

from ecommerce_api.dependencies.redis_connection import redis_conn


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
    name: str
    price: float
    quantity: int
    description: Optional[str] = None

    class Meta:
        """
        connecting Product class to redis db
        """
        database = redis_conn


# prod1 = Product(
#     name="hello",
#     price=1,
#     quantity=100
# )
#
# prod1.save()


class Order(HashModel):
    """
    Order schema
    """
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        """
        connecting product class to redis db
        """
        database = redis_conn


class User(BaseModel):
    """
    User schema
    """
    fullname: str = Field(default=None, index=True)
    email: EmailStr = Field(default=None, index=True)
    password: str = Field(default=None, index=True)
    join_date: datetime = datetime.now()

    class Config:
        """
        Config format class for User class
        """
        the_schema = {
            "user_demo": {
                "name": "YourName",
                "email": "email@example.com",
                "password": "1234"
            }
        }


class UserLogin(BaseModel):
    """
    User login schema
    """
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        """
        Config format class for User class
        """
        the_schema = {
            "user_demo": {
                "email": "email@example.com",
                "password": "1234"
            }
        }
