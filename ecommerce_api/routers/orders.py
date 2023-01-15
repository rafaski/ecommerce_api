from fastapi import Request, APIRouter, Depends

from ecommerce_api.schemas import Output, JWTData
from ecommerce_api.dependencies.slack_connection import post_to_slack
from ecommerce_api.sql.operations import OrderOperations, ProductOperations
from ecommerce_api.auth.access import authorize_token, admin_access_only
from ecommerce_api.errors import NotFound

router = APIRouter(tags=["orders"])


@router.get("/order/add", response_model=Output)
async def add_item(
    request: Request,
    product_id: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Add item to shopping cart
    """
    product = ProductOperations.get_by_id(product_id=product_id)
    if not product:
        raise NotFound(details="Product not found")
    if product.quantity <= 0:
        raise NotFound(details="Product out of stock")
    OrderOperations.add(product_id=product_id)
    return Output(success=True, message="Item added to cart")


@router.get("/order/{email}", response_model=Output)
async def get_all_items(
    request: Request,
    email: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Returns all items in user's shopping cart
    """
    items = OrderOperations.get_all(email=email)
    return Output(success=True, results=items)


@router.delete("/order/remove/{product_id}", response_model=Output)
async def remove_item(
    request: Request,
    email: str,
    product_id: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Removes item from cart
    """
    OrderOperations.remove_item(email=email, product_id=product_id)
    return Output(success=True, message="Item deleted from cart")


@router.post("/order/cancel/{order_id}", response_model=Output)
async def cancel_order(
    request: Request,
    order_id: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Cancel order
    """
    OrderOperations.cancel(order_id=order_id)
    return Output(success=True, message="Order cancelled")


@router.post("/order/submit", response_model=Output)
async def submit_order(
    request: Request,
    email: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Submit new order
    """
    order = OrderOperations.submit(email=email)
    await post_to_slack(order=order)
    return Output(success=True, results=order)


@router.get("/order/all", response_model=Output)
@admin_access_only
async def get_all(request: Request, data: JWTData = Depends(authorize_token)):
    """
    Get all orders
    """
    order = OrderOperations.get_all()
    return Output(success=True, results=order)


@router.get("/order/{order_id}", response_model=Output)
@admin_access_only
async def get_all(
        request: Request,
        order_id: str, data:
        JWTData = Depends(authorize_token)
):
    """
    Get order from order_id
    """
    order = OrderOperations.get(order_id=order_id)
    return Output(success=True, results=order)






