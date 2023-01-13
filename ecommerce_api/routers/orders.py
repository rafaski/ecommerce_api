from fastapi import Request, APIRouter, Depends

from ecommerce_api.schemas import Output, JWTData
from ecommerce_api.dependencies.slack_connection import post_to_slack
from ecommerce_api.sql.operations import (
    make_order, get_all_user_orders, get_all_orders
)
from ecommerce_api.auth.access import authorize_token, admin_access_only

router = APIRouter(tags=["orders"])


@router.get("/orders/all", response_model=Output)
async def get_order(
    request: Request,
    email: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Returns all placed orders by user
    """
    result = get_all_user_orders(email=email)
    return Output(success=True, results=result)


@router.post("/orders/new", response_model=Output)
async def create_order(
    request: Request,
    email: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Place an order
    """
    result = make_order(email=email)
    await post_to_slack(order=result)
    return Output(success=True, results=result)


@router.get("/orders/all", response_model=Output)
@admin_access_only
async def get_all(request: Request, data: JWTData = Depends(authorize_token)):
    """
    Get all orders
    """
    result = get_all_orders()
    return Output(success=True, results=result)






