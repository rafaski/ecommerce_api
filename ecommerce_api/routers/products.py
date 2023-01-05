from fastapi import APIRouter, Request, Depends

from ecommerce_api.schemas import Product
from ecommerce_api.schemas import Output
from ecommerce_api.auth.jwt_handler import sign_jwt
from ecommerce_api.auth.jwt_bearer import JwtBearer

router = APIRouter()

# TODO: Can redis cloud operations be awaited? Add auth Depends to post endpoints


@router.post("/create_product", response_model=Output)
async def create_product(request: Request, product: Product):
    """
    Creates new product
    """
    return Output(success=True, results=product.save())


@router.get("/products", response_model=Output)
async def get_all_products(request: Request):
    """
    Get a list of all products
    """
    products = []

    # def create_product_format(pk: str):
    #     """
    #     Formats fields for creating new product
    #     :param pk: product primary key
    #     :return: product in JSON for redis storage
    #     """
    #     product = Product.get(pk)
    #     product_format = {
    #         "id": product.pk,
    #         "name": product.name,
    #         "price": product.price,
    #         "quantity": product.quantity
    #     }
    #     return product_format

    # for pk in Product.all_pks():
    #     products.append(create_product_format(pk))
    if products:
        for pk in Product.all_pks():
            product = Product.get(pk=pk)
            products.append(product)
    else:
        products = "No products"
    return Output(success=True, results=products)


@router.get("/products/{pk}", response_model=Output)
async def get_product_by_id(request: Request, pk: str):
    """
     Return a product by a primary key
    """
    product = Product.get(pk)
    return Output(success=True, results=product)


@router.delete("/products/{pk}", response_model=Output)
async def get_product_by_id(request: Request, pk: str):
    """
    Delete product by a primary key
    """
    product = Product.get(pk)
    return Output(success=True, results=product.delete(pk))
