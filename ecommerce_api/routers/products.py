from fastapi import APIRouter, Request

from ecommerce_api.schemas import Product, Output
from ecommerce_api.enums import ProductCategory
from ecommerce_api.errors import NotFound

router = APIRouter(tags=["products"])


def format_results(payload):
    """
    Returns list of products in dict() format.
    """
    response = []
    for product in payload:
        response.append(product.dict())
    return response


@router.get("/products/all", response_model=Output)
async def get_all(request: Request):
    """
    Get a list of all products
    """
    products = []
    stored_products = await Product.all_pks()
    async for product_id in stored_products:
        product = await Product.get(pk=product_id)
        products.append(product)
    return Output(success=True, results=products)


@router.get("/products/{product_id}", response_model=Output)
async def get_by_id(request: Request, product_id: str):
    """
     Return a product by a primary key
    """
    product = await Product.get(pk=product_id)
    if not product:
        raise NotFound()
    return Output(success=True, results=product)


@router.get("/products/{category}", response_model=Output)
async def get_by_category(category: ProductCategory):
    """
    Get all products by category
    """
    products = await Product.find(Product.category == category).all()
    matching_products = format_results(payload=products)
    return Output(success=True, results=matching_products)


@router.get("/products/{name}", response_model=Output)
async def get_by_name(name: str):
    """
    Get all products with matching phrase in name
    """
    products = await Product.find(Product.name % name).all()
    matching_products = format_results(payload=products)
    return Output(success=True, results=matching_products)
