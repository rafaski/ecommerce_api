from fastapi import FastAPI

from ecommerce_api.routers.root import router as root_router
from ecommerce_api.routers.admin import router as admin_router
from ecommerce_api.routers.login import router as users_router
from ecommerce_api.routers.products import router as products_router
from ecommerce_api.routers.orders import router as orders_router
from ecommerce_api.dependencies.redis_connection import redis_cache

description = """
E-commerce API allows you to:

* as user: signup and login to use services
* as user: make an authorized order
* as admin: manage product inventory (create, update, delete), orders and users

To access /admin endpoints you'll need admin credentials
To access /orders endpoints signup to receive access token.
"""

app = FastAPI(
    title="E-commerce API",
    description=description
)

app.include_router(root_router)
app.include_router(admin_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)


@app.on_event("startup")
async def startup():
    # TODO: add redis caching with fastapi_cache
    # FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")
    pass

