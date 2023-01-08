import jwt
from passlib.hash import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import NoReturn

from ecommerce_api.dependencies.mongodb_connection import get_user
from ecommerce_api.settings import JWT_SECRET_KEY, ALGORITHM
from ecommerce_api.errors import Unauthorized

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(email: str, password: str) -> NoReturn | dict:
    user = await get_user(email=email)
    if not user:
        raise Unauthorized()
    if not bcrypt.verify(secret=password, hash=user.get(password)):
        raise Unauthorized()
    return user

# users = await get_all_users()
#     for u in users:
#         if not user.email == u.email and user.password == u.password:
#             raise Unauthorized()

# async def get_current_user(token: str = Depends(oauth_scheme)) -> :
#     try:
#         payload = jwt.decode(
#             payload=token,
#             key=JWT_SECRET_KEY,
#             algorithm=ALGORITHM
#         )
#         user = await get_user(email=email)
