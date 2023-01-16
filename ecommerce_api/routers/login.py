from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ecommerce_api.schemas import Output, User
from ecommerce_api.auth.user_pass import verify
from ecommerce_api.errors import Unauthorized, BadRequest
from ecommerce_api.sql.operations import UserOperations
from ecommerce_api.auth.access import create_token

router = APIRouter(tags=["login"])


@router.post("/signup", response_model=Output)
async def user_signup(request: Request, user: User):
    """
    User sign up
    """
    existing_user = UserOperations.get_by_email(email=user.email)
    if not existing_user:
        UserOperations.create(user=user)
        return Output(success=True, results=user)
    raise BadRequest(details=f"User {user.email} already exists!")


@router.post("/login", response_model=Output)
async def user_login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    User login via Oauth2 form.
    JWT token required for authentication.
    """
    existing_user = UserOperations.get_by_email(email=form_data.username)
    if not existing_user:
        raise Unauthorized(details=(
            f"User {form_data.username} does not exist. "
            f"Create an account first."
        ))
    if not verify(
        password=form_data.password,
        hashed_password=existing_user.password
    ):
        raise Unauthorized(details="Invalid credentials")
    token = create_token(user=existing_user)
    return Output(
        success=True,
        results={'access_token': token, 'token_type': 'bearer'})
