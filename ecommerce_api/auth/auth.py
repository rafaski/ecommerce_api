from passlib.hash import bcrypt

from ecommerce_api.dependencies.mongodb_connection import get_user


async def authenticate_user(email: str, password: str):
    user = await get_user(email=email)
    if not user:
        return False
    if not bcrypt.verify(password, user.password):
        return False
    return user
