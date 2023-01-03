from fastapi import FastAPI, Request
from fastapi.background import BackgroundTasks
import httpx
import time

from ecommerce_api.dependencies.redis_connection import redis
from ecommerce_api.schemas import Order
from ecommerce_api.enums import OrderStatus

description = """
Payments  API

To mimic behavior of separate applications change port number and run with:
"uvicorn microservices.payments:app --reload --port=8001" 
"""

app = FastAPI(
    title="Payment microservice API",
)


LOCAL_HOST = "http://localhost:8000/"


@app.get("/orders/{pk}")
def get_order(pk: str) -> Order:
    """
    Return an order based on order primary key
    :param pk: order primary key
    :return: order based on order primary key
    """
    order = Order.get(pk)
    redis.xadd("refund_order", order.dict(), "*")
    return order


@app.post("/orders")
async def create_order(
        request: Request,
        background_tasks: BackgroundTasks
) -> Order:
    """
    Create order. Pass product primary key and order quantity in request body.
    """
    endpoint = "products/"
    body = await request.json()
    async with httpx.AsyncClient() as client:
        req = await client.get(
            url=f"{LOCAL_HOST}{endpoint}{body.get('id')}"
        )
    product = req.json()
    order = Order(
        product_id=body.get("id"),
        price=product.price,
        fee=0.2*product.price,
        total=1.2*product.price,
        quantity=body.get("quantity"),
        status=OrderStatus.PENDING
    )
    order.save()

    def order_completed(order: Order):
        time.sleep(5)
        order.status = OrderStatus.COMPLETED
        order.save()
        redis.xadd("order_completed", order.dict(), "*")

    background_tasks.add_task(order_completed, order)

    return order





