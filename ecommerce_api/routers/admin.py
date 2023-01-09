from fastapi import APIRouter, Request, Depends

from ecommerce_api.schemas import Product, Order, Output
from ecommerce_api.errors import NotFound
from ecommerce_api.dependencies.mongodb_connection import (
    get_user, get_all_users, remove_user
)
from ecommerce_api.auth.auth import authenticate_admin

router = APIRouter(
    tags=["admin"],
    prefix="/admin",
    dependencies=[Depends(authenticate_admin)]
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
    Delete product by product id (primary key)
    """
    product = await Product.get(pk=product_id)
    if not product:
        raise NotFound()
    await product.delete(pk=product_id)
    return Output(success=True, message="Product deleted")


@router.get("/orders/all", response_model=Output)
async def get_all(request: Request, order_id: str):
    """
    Get all orders
    """
    orders = []
    stored_orders = await Order.all_pks()
    async for product_id in stored_orders:
        order = await Order.get(pk=order_id)
        orders.append(order)
    return Output(success=True, results=orders)


@router.get("/orders/{order_id}", response_model=Output)
async def get_by_id(request: Request, order_id: str):
    """
    Get an order by order id (primary key)
    """
    order = await Order.get(pk=order_id)
    if not order:
        raise NotFound()
    return Output(success=True, results=order)


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
        raise NotFound()
    return Output(success=True, results=user)


@router.delete("/users/{email}", response_model=Output)
async def delete_user(request: Request, email: str):
    """
    Returns user info from database
    """
    await remove_user(email=email)
    return Output(success=True, message="User removed")
