from fastapi import APIRouter, Request, Depends

from ecommerce_api.schemas import Output, Product, User, Login
from ecommerce_api.enums import ProductCategory
from ecommerce_api.errors import NotFound
from ecommerce_api.sql.operations import (
    get_product_by_id, get_products_by_category, get_all_products,
    remove_product
)
from ecommerce_api.auth.jwt_handler import get_current_user
from ecommerce_api.auth.validation import admin_access

router = APIRouter(tags=["products"])


@router.get("/products/all", response_model=Output)
async def get_all(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """
    Get a list of all products
    """
    products = await get_all_products()
    return Output(success=True, results=products)


@router.get("/products/{product_id}", response_model=Output)
async def get_by_id(
    request: Request,
    product_id: str,
    current_user: User = Depends(get_current_user)
):
    """
     Return a product by a primary key
    """
    product = await get_product_by_id(product_id=product_id)
    if not product:
        raise NotFound(details="Product not found")
    return Output(success=True, results=product)


@router.get("/products/{category}", response_model=Output)
async def get_by_category(
    category: ProductCategory,
    current_user: User = Depends(get_current_user)
):
    """
    Get all products by category
    """
    matching_products = await get_products_by_category(category=category)
    return Output(success=True, results=matching_products)


@router.post("/products/new", response_model=Output)
async def create_product(
    request: Request,
    product: Product,
    admin: Login = Depends(admin_access)
):
    """
    Create new product
    """
    new_product = Product(
        product_id=product.product_id,
        name=product.name,
        quantity=product.quantity,
        category=product.category,
        description=product.description,
        price=product.price,
        date_posted=product.created_date
    )
    await create_product(product=new_product)
    return Output(success=True, results=new_product)


@router.put("/products/{product_id}", response_model=Output)
async def update_product(
    request: Request,
    product_id: str,
    product: Product,
    admin: Login = Depends(admin_access)
):
    """
    Update existing product
    """
    updated_product = await update_product(
        product_id=product_id,
        product=product
    )
    return Output(success=True, results=updated_product)


@router.delete("/products/{product_id}", response_model=Output)
async def delete_product(
    request: Request,
    product_id: str,
    admin: Login = Depends(admin_access)
):
    """
    Delete product by product id (primary key)
    """
    product = await get_product_by_id(product_id=product_id)
    if not product:
        raise NotFound(details="Product not found")
    await remove_product(product_id=product_id)
    return Output(success=True, message="Product deleted")