from fastapi import FastAPI

from ecommerce_api.schemas import Output
from ecommerce_api.routers.products import router as inventory_router
from ecommerce_api.routers.users import router as users_router
from ecommerce_api.routers.root import router as root_router

description = """
Microservices API

tbc
"""

app = FastAPI(
    title="Microservices API",
    description=description
)

app.include_router(inventory_router)
app.include_router(users_router)
app.include_router(root_router)
