from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any, List
from datetime import datetime
from uuid import uuid4

from ecommerce_api.enums import ProductCategory, UserType


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
    email: EmailStr
    password: str
    orders: List[dict]

    @property
    def type(self) -> UserType:
        return UserType.CUSTOMER

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
    id: str = str(uuid4())[:8]
    name: str
    quantity: int = Field(ge=0)
    category: ProductCategory
    description: Optional[str] = None
    price: float

    class Config:
        orm_true = True


class Order(BaseModel):
    """
    Order schema
    """
    id: str = str(uuid4())[:8]
    created_date: datetime
    total_price: float
    user_email: str
    status: str
    product_id: str
    products: List[Product] = []
    total_items: int = Field(ge=1)

    class Config:
        orm_true = True


class Login(BaseModel):
    """
    Login schema
    """
    email: str
    password: str


class JWTData(BaseModel):
    """
    Token schema that accepts user email
    """
    email: Optional[str]
    user_type: UserType






