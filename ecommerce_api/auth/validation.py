from passlib.hash import bcrypt
from fastapi import Depends
from fastapi.security import (
    HTTPBasic, HTTPBasicCredentials
)
from typing import NoReturn
import secrets

from ecommerce_api.errors import Unauthorized, BadRequest
from ecommerce_api.dependencies.mongodb_connection import get_user
from ecommerce_api.settings import ADMIN_USERNAME, ADMIN_SECRET_KEY
from ecommerce_api.sql.operations import get_user_by_email

security = HTTPBasic()


async def verify_user_exists(email: str) -> bool:
    user = await get_user_by_email(email=email)
    if user:
        raise BadRequest(details="Email already exists")
    return True


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


def admin_access(
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


