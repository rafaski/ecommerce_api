from fastapi import APIRouter, Request, Depends

from ecommerce_api.schemas import Output, Login
from ecommerce_api.errors import NotFound
from ecommerce_api.sql.operations import (
    get_user_by_email, get_users, remove_user
)
from ecommerce_api.auth.validation import admin_access

router = APIRouter(tags=["users"])


@router.get("/users/all", response_model=Output)
async def all_users(
    request: Request,
    admin: Login = Depends(admin_access)
):
    """
    Returns a list of all signed-up users
    """
    users = await get_users()
    return Output(success=True, results=users)


@router.get("/users/{email}", response_model=Output)
async def get_user(
    request: Request,
    email: str,
    admin: Login = Depends(admin_access)
):
    """
    Returns user info from database
    """
    user = await get_user_by_email(email=email)
    if not user:
        raise NotFound(details="User not found")
    return Output(success=True, results=user)


@router.delete("/users/{email}", response_model=Output)
async def delete_user(
    request: Request,
    email: str,
    admin: Login = Depends(admin_access)
):
    """
    Returns user info from database
    """
    user = await get_user_by_email(email=email)
    if not user:
        raise NotFound(details="User not found")
    await remove_user(email=email)
    return Output(success=True, message="User deleted")