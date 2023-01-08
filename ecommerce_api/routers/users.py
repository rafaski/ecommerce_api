from fastapi import APIRouter, Request
from passlib.hash import bcrypt

from ecommerce_api.schemas import Output
from ecommerce_api.schemas import User, UserLogin
from ecommerce_api.auth.jwt_handler import sign_jwt
from ecommerce_api.errors import Unauthorized
from ecommerce_api.dependencies.mongodb_connection import (
    create_user, get_all_users
)

router = APIRouter(tags=["user"])


@router.post("/user/signup", response_model=Output)
async def user_signup(request: Request, user: User):
    """
    User signup, secure hashed password
    """
    new_user = User(
        email=user.email,
        password=bcrypt(user.password)
    )
    await create_user(user=new_user)
    user_signed = sign_jwt(email=user.email)
    return Output(success=True, results=user_signed)


@router.post("/user/login", response_model=Output)
async def user_login(request: Request, user: UserLogin):
    users = await get_all_users()
    for u in users:
        if not user.email == u.email and user.password == u.password:
            raise Unauthorized()
    user_signed = sign_jwt(email=user.email)
    return Output(success=True, results=user_signed)
