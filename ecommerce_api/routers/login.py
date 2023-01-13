from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ecommerce_api.schemas import Output, User
from ecommerce_api.errors import NotFound, Unauthorized
from ecommerce_api.sql.operations import create_user, get_user_by_email
from ecommerce_api.auth.validation import verify_user_exists
from ecommerce_api.auth.hashing import verify_password
from ecommerce_api.auth.jwt_handler import create_access_token

router = APIRouter(tags=["login"])


@router.post("/signup", response_model=Output)
async def user_signup(request: Request, user: User):
    """
    User sign up
    """
    user_check = await verify_user_exists(email=user.email)
    if user_check:
        new_user = User(
            name=user.name,
            email=user.email,
            password=user.password
        )
        await create_user(user=new_user)
        return Output(success=True, results=new_user)


@router.post("/login", response_model=Output)
async def user_login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    User login via Oauth2 form.
    JWT token required for authentication.
    """
    user = await get_user_by_email(email=form_data.username)
    if not user:
        raise NotFound(details="Invalid credentials")
    if not verify_password(
            password=form_data.password,
            hashed_password=user.password
    ):
        raise Unauthorized(details="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return Output(
        success=True,
        results={'access_token': token, 'token_type': 'bearer'})
