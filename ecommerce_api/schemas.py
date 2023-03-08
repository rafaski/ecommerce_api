from pydantic import BaseModel, EmailStr, Field
from typing import Any
from datetime import datetime
from uuid import uuid4

from ecommerce_api.enums import ProductCategory, UserType, OrderStatus


class Output(BaseModel):
    """
    default endpoint return schema
    """
    success: bool
    message: str | None = None
    results: Any | None = None


class User(BaseModel):
    """
    User schema
    """
    email: EmailStr
    password: str

    @property
    def type(self) -> str:
        return UserType.ADMIN

    def dict(self, *args, **kwargs):
        _dict = super().dict()
        _dict.update({"type": self.type})
        return _dict

    class Config:
        """
        Without orm_mode, if you returned a SQLAlchemy model from your
        path operation, it wouldn't include the relationship data.
        """
        orm_true = True

    # def dict(self, *args, **kwargs):
    #     data = self.dict(*args, **kwargs)
    #     data["password"] = to_hash(data["password"])
    #     return data


class Product(BaseModel):
    """
    Product schema
    """
    name: str
    quantity: int = Field(ge=0)
    category: ProductCategory
    description: str | None = None
    price: float

    @property
    def id(self) -> str:
        return str(uuid4())[:8]

    def dict(self, *args, **kwargs):
        _dict = super().dict()
        _dict.update({"id": self.id})
        return _dict

    class Config:
        orm_true = True


class Order(BaseModel):
    """
    Order schema
    """
    id: str = str(uuid4())[:8]
    total_price: float = 0.0
    status: OrderStatus = OrderStatus.IN_PROGRESS
    user_email: str

    @property
    def created_date(self) -> datetime:
        return datetime.now()

    def dict(self, *args, **kwargs):
        _dict = super().dict()
        _dict.update({"created_date": self.created_date})
        return _dict

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
    email: str | None
    user_type: UserType






