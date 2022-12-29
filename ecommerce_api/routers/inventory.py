from fastapi import APIRouter, Request, Depends

from ecommerce_api.schemas import Product
from ecommerce_api.auth.jwt_handler import sign_jwt
from ecommerce_api.auth.jwt_bearer import JwtBearer

router = APIRouter()

# TODO: Can redis cloud operations be awaited? Add auth Depends to post endpoints


@router.get("/products/{pk}")
async def get_product_by_id(request: Request, pk: str) -> Product:
    """
     Return a product by a primary key
    """
    product = Product.get(pk)
    return product


@router.get("/products")
async def get_all_products(request: Request) -> list:
    """
    Get a list of all products
    """
    products = []

    def create_product_format(pk: str):
        """
        Formats fields for creating new product
        :param pk: product primary key
        :return: product in JSON for redis storage
        """
        product = Product.get(pk)
        product_format = {
            "id": product.pk,
            "name": product.name,
            "price": product.price,
            "available_quantity": product.available_quantity
        }
        return product_format

    for pk in Product.all_pks():
        products.append(create_product_format(pk))
    return products


@router.post("/create_product")
async def create_product(request: Request, product: Product) -> Product:
    """
    Creates new product
    """
    return product.save()


@router.delete("/products/{pk}")
async def get_product_by_id(request: Request, pk: str):
    """
    Delete product by a primary key
    """
    product = Product.get(pk)
    return product.delete(pk)
