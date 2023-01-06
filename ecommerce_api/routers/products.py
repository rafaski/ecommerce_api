from fastapi import APIRouter, Request
from aredis_om import NotFoundError

from ecommerce_api.schemas import Product
from ecommerce_api.schemas import Output
from ecommerce_api.enums import Category

router = APIRouter()


@router.get("/products", response_model=Output)
async def get_all_products(request: Request):
    """
    Get a list of all products
    """
    products = []
    try:
        for pk in Product.all_pks():
            product = await Product.get(pk=pk)
            products.append(product)
    except NotFoundError:
        return Output(success=False, message="No products found")
    return Output(success=True, results=products)


@router.get("/products/{pk}", response_model=Output)
async def get_product_by_id(request: Request, pk: str):
    """
     Return a product by a primary key
    """
    try:
        product = await Product.get(pk)
    except NotFoundError:
        return Output(success=False, message="No product with this ID")
    return Output(success=True, results=product)


def format_results(payload):
    """
    Returns list of products in dict() format.
    """
    response = []
    for product in payload:
        response.append(product.dict())
    return response


@router.get("/products/category", response_model=Output)
async def get_category(category: Category):
    """
    Get all products by category
    """
    products = await Product.find(Product.category == category).all()
    matching_products = format_results(products)
    return Output(success=True, results=matching_products)


@router.get("/products/name", response_model=Output)
async def get_name(name: str):
    """
    Get all products with matching phrase in name
    """
    products = await Product.find(Product.name % name).all()
    matching_products = format_results(products)
    return Output(success=True, results=matching_products)
