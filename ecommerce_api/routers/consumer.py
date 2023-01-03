import time

from ecommerce_api.dependencies.redis_connection import redis
from ecommerce_api.schemas import Product

KEY = "order_completed"
GROUP = "inventory-group"

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
                try:
                    product = Product.get(obj.get("product_id"))
                    product.available_quantity -= int(obj.get("available_quantity"))
                    product.save()
                except:
                    redis.xadd("refund_order", obj, "*")

    except Exception as e:
        print(str(e))
    time.sleep(1)




