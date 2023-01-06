from fastapi import APIRouter, Request

from ecommerce_api.schemas import Output
from ecommerce_api.schemas import User, UserLogin
from ecommerce_api.auth.jwt_handler import sign_jwt
from ecommerce_api.errors import Unauthorized

router = APIRouter()

USERS = []


@router.post("/user/signup", response_model=Output, tags=["user"])
def user_signup(request: Request, user: User):
    """
    User signup
    """
    USERS.append(user)
    user_signed = sign_jwt(user.email)
    return Output(success=True, results=user_signed)


@router.post("/user/login", response_model=Output, tags=["user"])
def user_login(request: Request, user: UserLogin):
    for x in USERS:
        if not user.email == x.email and user.password == x.password:
            raise Unauthorized()
    user_signed = sign_jwt(user.email)
    return Output(success=True, results=user_signed)
