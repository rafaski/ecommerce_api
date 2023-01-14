from fastapi import APIRouter, Request, Depends

from ecommerce_api.schemas import Output, Product, JWTData
from ecommerce_api.enums import ProductCategory
from ecommerce_api.errors import NotFound
from ecommerce_api.sql.operations import ProductOperations
from ecommerce_api.auth.access import authorize_token, admin_access_only

router = APIRouter(
    tags=["products"]
)


@router.get("/products/all", response_model=Output)
async def get_all(
    request: Request,
    data: JWTData = Depends(authorize_token)
):
    """
    Get a list of all products
    """
    products = ProductOperations.get_all()
    return Output(success=True, results=products)


@router.get("/products/{product_id}", response_model=Output)
async def get_by_id(
    request: Request,
    product_id: str,
    data: JWTData = Depends(authorize_token)
):
    """
     Return a product by a primary key
    """
    product = ProductOperations.get_by_id(product_id=product_id)
    if not product:
        raise NotFound(details=f"Product with ID {product_id} not found")
    return Output(success=True, results=product)


@router.get("/products/{category}", response_model=Output)
async def get_by_category(
    category: ProductCategory,
    data: JWTData = Depends(authorize_token)
):
    """
    Get all products by category
    """
    matching_products = ProductOperations.get_by_category(category=category)
    return Output(success=True, results=matching_products)


@router.post("/products/new", response_model=Output)
@admin_access_only
async def create_new_product(
    request: Request,
    product: Product,
    data: JWTData = Depends(authorize_token)
):
    """
    Create new product
    """
    ProductOperations.create(product=product)
    return Output(success=True, results=product)


@router.put("/products/{product_id}", response_model=Output)
@admin_access_only
async def update_product(
    request: Request,
    product_id: str,
    product: Product,
    data: JWTData = Depends(authorize_token)
):
    """
    Update existing product
    """
    updated_product = ProductOperations.update(
        product_id=product_id,
        product=product
    )
    return Output(success=True, results=updated_product)


@router.delete("/products/{product_id}", response_model=Output)
@admin_access_only
async def delete_product(
    request: Request,
    product_id: str,
    data: JWTData = Depends(authorize_token)
):
    """
    Delete product by product id (primary key)
    """
    product = ProductOperations.get_by_id(product_id=product_id)
    if not product:
        raise NotFound(details="Product not found")
    ProductOperations.remove(product_id=product_id)
    return Output(success=True, message="Product deleted")
