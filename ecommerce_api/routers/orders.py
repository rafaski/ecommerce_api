from fastapi import Request, APIRouter, Depends

from ecommerce_api.schemas import Order, Product
from ecommerce_api.enums import OrderStatus
from ecommerce_api.schemas import Output
from ecommerce_api.auth.jwt_bearer import JwtBearer

router = APIRouter()


@router.get("/orders/{pk}", response_model=Output, tags=["orders"])
def get_order(request: Request, pk: str):
    """
    Returns order based on order primary key
    """
    order = Order.get(pk)
    return Output(success=True, results=order)


@router.post(
    "/orders",
    response_model=Output,
    dependencies=[Depends(JwtBearer())],
    tags=["orders"]
)
async def create_order(request: Request, order: Order):
    """
    Create order. Pass product primary key and order quantity in request body.
    Requires signed and validated JWT.
    """

    for pk in Product.all_pks():
        if pk == order.product_id:
            product = Product.get(pk)

            new_order = Order(
                product_id=order.product_id,
                price=order.price,
                quantity=order.quantity,
                total=order.price * order.quantity,
                status=OrderStatus.PENDING
            )

            product.quantity -= new_order.quantity
            await product.save()
    await order.save()
    return Output(success=True, results=order)





