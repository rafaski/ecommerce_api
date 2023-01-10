import httpx
from typing import NoReturn

from ecommerce_api.settings import SLACK_WEBHOOK_URL
from ecommerce_api.schemas import Order


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
        connection = await client.post(
            url=SLACK_WEBHOOK_URL,
            data=data
        )
