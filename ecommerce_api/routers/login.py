from fastapi import APIRouter, Request
from passlib.hash import bcrypt

from ecommerce_api.schemas import Output, User, UserLogin
from ecommerce_api.auth.jwt_handler import sign_jwt
from ecommerce_api.dependencies.mongodb_connection import (
    create_user
)
from ecommerce_api.auth.auth import verify_login

router = APIRouter(tags=["login"])


@router.post("/signup", response_model=Output)
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


@router.post("/login", response_model=Output)
async def user_login(request: Request, user: UserLogin):
    await verify_login(email=user.email, password=user.password)
    user_signed = sign_jwt(email=user.email)
    return Output(success=True, results=user_signed)
