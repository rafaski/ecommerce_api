import jwt
from passlib.hash import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import NoReturn

from ecommerce_api.settings import JWT_SECRET_KEY, ALGORITHM
from ecommerce_api.errors import Unauthorized
from ecommerce_api.dependencies.mongodb_connection import (
    get_user, get_all_users
)

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(email: str, password: str) -> NoReturn | dict:
    user = await get_user(email=email)
    if not user:
        raise Unauthorized()
    if not bcrypt.verify(secret=password, hash=user.get(password)):
        raise Unauthorized()
    return user


async def verify_login(email: str, password: str) -> bool:
    users = await get_all_users()
    for user in users:
        if not user.email == email and user.password == password:
            raise Unauthorized()
    return True

# async def get_current_user(token: str = Depends(oauth_scheme)) -> :
#     try:
#         payload = jwt.decode(
#             payload=token,
#             key=JWT_SECRET_KEY,
#             algorithm=ALGORITHM
#         )
#         user = await get_user(email=email)
