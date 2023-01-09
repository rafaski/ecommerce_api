from fastapi import Request, APIRouter, Depends

from ecommerce_api.schemas import Order, Product,Output
from ecommerce_api.errors import BadRequest
from ecommerce_api.auth.auth import get_current_user

router = APIRouter(tags=["orders"], dependencies=[Depends(get_current_user)])


@router.get("/orders/{product_id}", response_model=Output)
def get_order(request: Request, product_id: str):
    """
    Returns order based on order primary key
    """
    order = Order.get(pk=product_id)
    return Output(success=True, results=order)


@router.post("/orders/new", response_model=Output)
async def create_order(request: Request, order: Order):
    """
    Create order. Pass product primary key and order quantity in request body.
    Requires signed and validated JWT.
    """
    product = await Product.get(order.product_id)
    if not product:
        raise BadRequest()

    product.quantity -= order.quantity
    await product.save()
    await order.save()
    return Output(success=True, results=order)





