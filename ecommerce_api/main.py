from fastapi import FastAPI

from ecommerce_api.routers.users import router as users_router
from ecommerce_api.routers.login import router as login_router
from ecommerce_api.routers.products import router as products_router
from ecommerce_api.routers.orders import router as orders_router

from ecommerce_api.sql.database import init_db, database

from ecommerce_api.dependencies.redis_connection import redis_cache

description = """
E-commerce API allows you to:

* as user: signup and login to use services
* as user: search for products, add products to cart, make order
* as admin: manage product inventory (create, update, delete), orders and users

Endpoints accessible for users require registration to receive access token.
Admin related endpoints require admin credentials.
"""

app = FastAPI(
    title="E-commerce API",
    docs_url="/",
    description=description
)


app.include_router(login_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)


# todo: error handling


@app.on_event("startup")
async def startup():
    # TODO: add redis caching with fastapi_cache
    # FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")
    init_db()


@app.on_event("shutdown")
async def shutdown():
    database.dispose_session()
