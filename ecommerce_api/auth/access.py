from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from functools import wraps

from ecommerce_api.schemas import JWTData, User
from ecommerce_api.enums import UserType
from ecommerce_api.errors import Unauthorized
from ecommerce_api.settings import JWT_SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_token(user: User) -> str:
    """
    Create JSON web token, returns signed JWT string
    """
    jwt_data = JWTData(email=user.email, user_type=user.type)
    encoded_jwt = jwt.encode(
        claims=jwt_data.dict(),
        key=JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt


def authorize_token(token: str = Depends(oauth2_scheme)) -> JWTData:
    """
    Decodes and verifies access token
    """
    try:
        payload = jwt.decode(
            token=token,
            key=JWT_SECRET_KEY,
            algorithms=ALGORITHM
        )
        if not payload:
            raise Unauthorized(details="Could not validate credentials")
        jwt_data = JWTData(**payload)
    except JWTError:
        raise Unauthorized(details="Could not validate credentials")
    return jwt_data


def admin_access_only(func):
    @wraps(func)
    async def _admin_access_only(*args, **kwargs):
        user_type = kwargs["data"].user_type
        if user_type == UserType.ADMIN:
            return await func(*args, **kwargs)
        raise Unauthorized(details="No access")
    return _admin_access_only

