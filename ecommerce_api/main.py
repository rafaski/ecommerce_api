from fastapi import FastAPI

from ecommerce_api.routers.products import router as inventory_router

description = """
Microservices API

tbc
"""

app = FastAPI(
    title="Microservices API",
    description=description
)

app.include_router(inventory_router)


@app.get("/")
def root():
    """
    Index page
    """
    return {"message": "Welcome to Microservices API. Go to /docs to test API"}
