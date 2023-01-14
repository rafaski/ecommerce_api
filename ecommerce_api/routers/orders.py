from fastapi import Request, APIRouter, Depends

from ecommerce_api.schemas import Output, JWTData
from ecommerce_api.dependencies.slack_connection import post_to_slack
from ecommerce_api.sql.operations import OrderOperations
from ecommerce_api.auth.access import authorize_token, admin_access_only

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
    OrderOperations.add_to_order(product_id=product_id)
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
    items = OrderOperations.get_all_items(email=email)
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


@router.get("/orders/{email}", response_model=Output)
async def get_all_per_user(
    request: Request,
    email: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Returns all placed orders by user
    """
    orders = OrderOperations.get_orders(email=email)
    return Output(success=True, results=orders)


@router.post("/orders/new", response_model=Output)
async def create_order(
    request: Request,
    email: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Place an order
    """
    order = OrderOperations.submit(email=email)
    await post_to_slack(order=order)
    return Output(success=True, results=order)


@router.get("/orders/all", response_model=Output)
@admin_access_only
async def get_all(request: Request, data: JWTData = Depends(authorize_token)):
    """
    Get all orders
    """
    order = OrderOperations.get_orders()
    return Output(success=True, results=order)






