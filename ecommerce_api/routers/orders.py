from fastapi import Request, APIRouter, Depends

from ecommerce_api.schemas import Output, User, Login
from ecommerce_api.dependencies.slack_connection import post_to_slack
from ecommerce_api.sql.operations import (
    make_order, get_all_user_orders, get_all_orders
)
from ecommerce_api.auth.jwt_handler import get_current_user
from ecommerce_api.auth.validation import admin_access

router = APIRouter(tags=["orders"])


@router.get("/orders/all", response_model=Output)
async def get_order(
    request: Request,
    email: str,
    current_user: User = Depends(get_current_user)
):
    """
    Returns all placed orders by user
    """
    result = await get_all_user_orders(email=email)
    return Output(success=True, results=result)


@router.post("/orders/new", response_model=Output)
async def create_order(
    request: Request,
    email: str,
    current_user: User = Depends(get_current_user)
):
    """
    Place an order
    """
    result = await make_order(email=email)
    await post_to_slack(order=result)
    return Output(success=True, results=result)


@router.get("/orders/all", response_model=Output)
async def get_all(request: Request, admin: Login = Depends(admin_access)):
    """
    Get all orders
    """
    result = await get_all_orders()
    return Output(success=True, results=result)






