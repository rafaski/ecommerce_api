from fastapi import APIRouter, Request, Depends
from aredis_om import NotFoundError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ecommerce_api.schemas import Product
from ecommerce_api.schemas import Output
from ecommerce_api.dependencies.mongodb_connection import (
    get_user, get_all_users,remove_user
)

router = APIRouter()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Generate admin access token
    """
    return Output(
        success=True,
        results={"access_token": form_data.username, "token_type": "bearer"}
    )


@router.post("/create_product", response_model=Output, tags=["admin"])
async def create_product(request: Request, product: Product):
    """
    Create new product
    """
    new_product = Product(
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        description=product.description,
    )
    await new_product.save()
    return Output(success=True, results=new_product)


@router.put("/products/{pk}", response_model=Output, tags=["admin"])
async def update_product(request: Request, pk: str, product: Product):
    """
    Update existing product
    """
    updated_product = Product.get(pk)
    updated_product.name = product.name
    updated_product.price = product.price
    updated_product.quantity = product.quantity
    updated_product.description = product.description

    await updated_product.save()
    return Output(success=True, results=updated_product)


@router.delete("/products/{pk}", response_model=Output, tags=["admin"])
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


@router.get("/users", response_model=Output, tags=["admin"])
async def all_users(request: Request):
    """
    Returns a list of all signed-up users
    """
    users = get_all_users()
    return Output(success=True, results=users)


@router.get("/users/{email}", response_model=Output, tags=["admin"])
async def get_user(request: Request, email: str):
    """
    Returns user info from database
    """
    user = get_user(email=email)
    return Output(success=True, results=user)


@router.delete("/users/{email}", response_model=Output, tags=["admin"])
async def delete_user(request: Request, email: str):
    """
    Returns user info from database
    """
    user = remove_user(email=email)
    return Output(success=True, message="User removed")
