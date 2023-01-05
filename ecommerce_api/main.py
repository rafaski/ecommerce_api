from fastapi import FastAPI

from ecommerce_api.schemas import Output
from ecommerce_api.routers.products import router as inventory_router
from ecommerce_api.routers.users import router as users_router

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


@app.get("/")
def root():
    """
    Index page
    """
    return Output(
        succes=True,
        messaage="Welcome to E-commerce API. Go to /docs to test API"

    )