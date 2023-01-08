from fastapi import FastAPI

from ecommerce_api.routers.root import router as root_router
from ecommerce_api.routers.admin import router as admin_router
from ecommerce_api.routers.login import router as users_router
from ecommerce_api.routers.products import router as products_router
from ecommerce_api.routers.orders import router as orders_router

description = """
E-commerce API

tbc
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

