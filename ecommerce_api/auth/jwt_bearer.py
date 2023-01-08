from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ecommerce_api.auth.jwt_handler import decode_jwt
from ecommerce_api.errors import Unauthorized


class JwtBearer(HTTPBearer):
    """
    Verification of the protected route.
    Check if the HTTP request is authorized.
    """
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JwtBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise Unauthorized()
            return credentials.credentials
        else:
            raise Unauthorized()

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        payload = decode_jwt(token=jwt_token)
        if payload:
            return True

