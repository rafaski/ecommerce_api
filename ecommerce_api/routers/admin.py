from fastapi import APIRouter, Request, Depends
from aredis_om import NotFoundError

from ecommerce_api.schemas import Product
from ecommerce_api.schemas import Output
from ecommerce_api.auth.jwt_handler import sign_jwt
from ecommerce_api.auth.jwt_bearer import JwtBearer

router = APIRouter()


@router.post("/create_product", response_model=Output)
async def create_product(request: Request, product: Product):
    """
    Creates new product
    """
    new_product = Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        description=product.description,
    )
    await new_product.save()
    return Output(success=True, results=new_product)


@router.put("/products/{pk}", response_model=Output)
async def update_product(request: Request, pk: str, product: Product):
    """
    Updates existing product
    """
    updated_product = Product.get(pk)
    updated_product.name = product.name
    updated_product.price = product.price
    updated_product.quantity = product.quantity
    updated_product.description = product.description

    await updated_product.save()
    return Output(success=True, results=updated_product)


@router.delete("/products/{pk}", response_model=Output)
async def get_product_by_id(request: Request, pk: str):
    """
    Delete product by a primary key
    """
    try:
        product = Product.get(pk)
    except NotFoundError:
        return Output(success=False, message="No product with this ID")
    await product.delete(pk)
    return Output(success=True, message="Product deleted")
