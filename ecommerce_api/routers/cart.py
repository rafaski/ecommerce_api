from fastapi import Request, APIRouter, Depends

from ecommerce_api.schemas import Output, JWTData
from ecommerce_api.sql.operations import (
    add_to_cart, get_all_items_in_cart, remove_cart_item
)
from ecommerce_api.auth.access import authorize_token


router = APIRouter(tags=["cart"])


@router.get("/cart/add", response_model=Output)
async def add_to_cart(
    request: Request,
    product_id: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Add product to shopping cart
    """
    result = add_to_cart(product_id=product_id)
    return Output(success=True, results=result)


@router.get("/cart", response_model=Output)
async def get_all_cart_items(
    request: Request,
    email: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Returns all items in user's shopping cart
    """
    result = get_all_items_in_cart(email=email)
    return Output(success=True, results=result)


@router.delete("/cart/{cart_item_id}", response_model=Output)
async def remove_item_from_cart(
    request: Request,
    email: str,
    cart_item_id: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Removes item from cart
    """
    remove_cart_item(cart_item_id=cart_item_id, email=email)
    return Output(success=True, message="Item deleted from cart")
