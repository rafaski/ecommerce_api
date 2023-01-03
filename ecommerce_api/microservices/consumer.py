import time

from ecommerce_api.dependencies.redis_connection import redis
from ecommerce_api.schemas import Order
from ecommerce_api.enums import OrderStatus

KEY = "refund_order"
GROUP = "payment-group"

try:
    redis.xgroup_create(KEY, GROUP)
except:
    print("Group already exists!")

while True:
    try:
        results = redis.xreadgroup(GROUP, KEY, {KEY: ">"}, None)

        if results:
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj.get("pk"))
                order.status = OrderStatus.REFUNDED
                order.save()

    except Exception as e:
        print(str(e))
    time.sleep(1)




