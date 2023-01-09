from passlib.hash import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import NoReturn

from ecommerce_api.errors import Unauthorized
from ecommerce_api.dependencies.mongodb_connection import get_user
from ecommerce_api.auth.jwt_handler import decode_jwt
# from ecommerce_api.settings import ADMIN_SECRET_KEY, ADMIN_USERNAME

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


async def authenticate_user(email: str, password: str) -> NoReturn | bool:
    """
    Authenticates user
    """
    user = await get_user(email=email)
    if not user:
        raise Unauthorized()
    if not bcrypt.verify(secret=password, hash=user.get(password)):
        raise Unauthorized()
    return True


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> NoReturn | bool:
    """
    Gets current user
    """
    payload = decode_jwt(token=token)
    payload = dict(payload)
    user = await get_user(email=payload.get("email"))
    if not user:
        raise Unauthorized()
    return True


