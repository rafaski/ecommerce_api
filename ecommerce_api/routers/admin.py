from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from ecommerce_api.schemas import Product
from ecommerce_api.schemas import Output
from ecommerce_api.auth.auth import authenticate_user
from ecommerce_api.errors import Unauthorized, NotFound
from ecommerce_api.settings import JWT_SECRET_KEY, ALGORITHM
from ecommerce_api.dependencies.mongodb_connection import (
    get_user, get_all_users, remove_user
)

router = APIRouter(tags=["admin"])

# TODO: admin should see all orders made by users


@router.post("/token", response_model=Output)
async def generate_token(form_data=Depends(OAuth2PasswordRequestForm)):
    """
    Generate admin access token
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise Unauthorized()
    token = jwt.encode(payload=user, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
    return Output(
        success=True,
        results={"access_token": token, "token_type": "bearer"}
    )


@router.post("/products/new", response_model=Output)
async def create_product(request: Request, product: Product):
    """
    Create new product
    """
    await product.save()
    return Output(success=True, results=product)


@router.put("/products/{product_id}", response_model=Output)
async def update_product(request: Request, product_id: str, product: Product):
    """
    Update existing product
    """
    updated_product = await Product.get(pk=product_id)
    updated_product.name = product.name
    updated_product.price = product.price
    updated_product.quantity = product.quantity
    updated_product.description = product.description

    await updated_product.save()
    return Output(success=True, results=updated_product)


@router.delete("/products/{product_id}", response_model=Output)
async def delete_product(request: Request, product_id: str):
    """
    Delete product by a primary key
    """
    product = await Product.get(pk=product_id)
    if not product:
        raise NotFound
    await product.delete(pk=product_id)
    return Output(success=True, message="Product deleted")


@router.get("/users/all", response_model=Output)
async def all_users(request: Request):
    """
    Returns a list of all signed-up users
    """
    users = await get_all_users()
    return Output(success=True, results=users)


@router.get("/users/{email}", response_model=Output)
async def get_user(request: Request, email: str):
    """
    Returns user info from database
    """
    user = await get_user(email=email)
    if not user:
        raise NotFound
    return Output(success=True, results=user)


@router.delete("/users/{email}", response_model=Output)
async def delete_user(request: Request, email: str):
    """
    Returns user info from database
    """
    await remove_user(email=email)
    return Output(success=True, message="User removed")
