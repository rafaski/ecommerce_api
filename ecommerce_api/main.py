from fastapi import FastAPI

from ecommerce_api.routers.users import router as users_router
from ecommerce_api.routers.login import router as login_router
from ecommerce_api.routers.products import router as products_router
from ecommerce_api.routers.orders import router as orders_router

from ecommerce_api.sql.database import init_db, database

description = """
### E-commerce API allows you to:

#### As a user: 
- Sign up and login to use services
- Search for products by id, name and category,
- Add items to cart,
- Remove items from cart,
- Get all items from cart,
- Cancel order,
- Submit order

#### As admin: 
- Get a list of all registered users
- Get user info
- Delete user's account
- Create new product
- Update product
- Delete product from inventory
- Get all orders
- Get order from order id

Register to receive access token.\n
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


# todo: error handling, redis caching with fastapi_cache


@app.on_event("startup")
async def startup():
    init_db()
    # FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")


@app.on_event("shutdown")
async def shutdown():
    database.dispose_session()
