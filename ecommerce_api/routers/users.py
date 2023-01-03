from fastapi import APIRouter, Body, Request

from ecommerce_api.schemas import Output
from ecommerce_api.schemas import User, UserLogin
from ecommerce_api.auth.jwt_handler import sign_jwt

router = APIRouter()

USERS = []


@router.post("/user/signup", response_model=Output)
def user_signup(request: Request, user: User = Body(default=None)):
    USERS.append(user)
    return Output(success=True, results=sign_jwt(user.email))


def check_user(request: Request, data: UserLogin):
    for user in USERS:
        if not user.email == data.email and user.password == data.password:
            return True
        return False


@router.post("/user/login", response_model=Output)
def user_login(request: Request, user: UserLogin = Body(default=None)):
    if check_user(user):
        return Output(success=True, results=sign_jwt(user.email))
    else:
        return Output(success=True, message={"error": "Invalid login details"})
