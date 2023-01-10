import httpx
from typing import NoReturn

from ecommerce_api.settings import SLACK_WEBHOOK_URL
from ecommerce_api.schemas import Order
from ecommerce_api.errors import BadRequest


def post_to_slack(order: Order) -> NoReturn:
    """
    Send notification to Slack channel when new order is placed
    """
    message = f"New order from Ecommerce API"
    data = {
        "title": message,
        "details": order
    }
    async with httpx.AsyncClient() as client:
        try:
            connection = await client.post(
                url=SLACK_WEBHOOK_URL,
                data=data
            )
        except httpx.HTTPError:
            raise BadRequest(details="Connection error")
