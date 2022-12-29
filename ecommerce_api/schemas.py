from redis_om import HashModel
from pydantic import BaseModel, Field, EmailStr

from ecommerce_api.redis_connection import redis


class Product(HashModel):
    """
    Product schema
    """
    name: str
    price: float
    available_quantity: int

    class Meta:
        """
        connecting product class to redis db
        """
        database = redis


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
        database = redis


class User(BaseModel):
    """
    User schema
    """
    fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

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
