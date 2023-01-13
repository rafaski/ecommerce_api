from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any, List
from datetime import datetime
from uuid import uuid4

from ecommerce_api.enums import ProductCategory


class Output(BaseModel):
    """
    default endpoint return schema
    """
    success: bool
    message: Optional[str] = None
    results: Optional[Any] = None


class User(BaseModel):
    """
    User schema
    """
    name: str
    email: EmailStr
    password: str

    class Config:
        """
        Without orm_mode, if you returned a SQLAlchemy model from your
        path operation, it wouldn't include the relationship data.
        """
        orm_true = True


class Product(BaseModel):
    """
    Product schema
    """
    product_id: str = str(uuid4())[:8]
    name: str
    quantity: int = Field(ge=0)
    category: ProductCategory
    description: Optional[str] = None
    price: float
    created_date: datetime = datetime.today()

    class Config:
        orm_true = True


class ShowCartItems(BaseModel):
    """
    ShowCartItems schema
    """
    cart_id: str = str(uuid4())[:8]
    products: Product
    created_date: datetime = datetime.today()

    class Config:
        orm_true = True


class ShowCart(BaseModel):
    """
    ShowCart schema
    """
    cart_id: str = str(uuid4())[:8]
    cart_items: List[ShowCartItems] = []

    class Config:
        orm_true = True


class OrderDetails(BaseModel):
    """
    Order Details schema
    """
    id: str = str(uuid4())[:8]
    order_id: str = str(uuid4())[:8]
    product_order_details: Product

    class Config:
        orm_true = True


class Order(BaseModel):
    """
    Order schema
    """
    id: Optional[str] = str(uuid4())[:8]
    order_date: datetime
    order_total: float
    order_status: str
    customer_email: str
    order_details: List[OrderDetails] = []
    quantity: int = Field(ge=1)

    class Config:
        orm_true = True


class Login(BaseModel):
    """
    Login schema
    """
    email: str
    password: str


class Token(BaseModel):
    """
    Access token schema
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Token schema that accepts user email
    """
    email: Optional[str]






