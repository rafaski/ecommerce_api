from fastapi import APIRouter, Request, Depends
from passlib.hash import bcrypt

from ecommerce_api.schemas import Output, User
from ecommerce_api.auth.jwt_handler import encode_jwt
from ecommerce_api.dependencies.mongodb_connection import (
    create_user
)
from ecommerce_api.auth.oauth import authenticate_user
from fastapi.security import OAuth2PasswordRequestForm

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
    token = encode_jwt(email=user.email)
    return Output(success=True, results=token)


@router.post("/login", response_model=Output)
async def user_login(
        request: Request,
        form_data=Depends(OAuth2PasswordRequestForm)
):
    """
    User login via Oauth2 form.
    JWT token required for authentication.
    """
    await authenticate_user(
        email=form_data.username,
        password=form_data.password
    )
    token = encode_jwt(email=form_data.username)
    return Output(
        success=True,
        results={'access_token': token, 'token_type': 'bearer'})
