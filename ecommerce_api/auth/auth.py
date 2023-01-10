from passlib.hash import bcrypt
from fastapi import Depends
from fastapi.security import (
    OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
)
from typing import NoReturn
import secrets

from ecommerce_api.errors import Unauthorized
from ecommerce_api.dependencies.mongodb_connection import get_user
from ecommerce_api.auth.jwt_handler import decode_jwt
from ecommerce_api.settings import ADMIN_USERNAME, ADMIN_SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
security = HTTPBasic()


async def authenticate_user(email: str, password: str) -> NoReturn | bool:
    """
    Authenticates user
    """
    user = await get_user(email=email)
    if not user:
        raise Unauthorized(details="Invalid email or password")
    if not bcrypt.verify(secret=password, hash=user.get(password)):
        raise Unauthorized(details="Invalid email or password")
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
        raise Unauthorized(details="Invalid user")
    return True


def authenticate_admin(
        credentials: HTTPBasicCredentials = Depends(security)
) -> bool:
    """
    Authenticate admin login with HTTP Basic Auth
    """
    if not secrets.compare_digest(credentials.username, ADMIN_USERNAME):
        raise Unauthorized(details="Invalid admin credentials")
    if not secrets.compare_digest(credentials.password, ADMIN_SECRET_KEY):
        raise Unauthorized(details="Invalid admin credentials")
    return True


