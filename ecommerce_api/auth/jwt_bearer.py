from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ecommerce_api.auth.jwt_handler import decode_jwt

"""
Verification of the protected route.
Check if the HTTP request is authorized.
"""


class JwtBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JwtBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid or expired token"
                )
            else:
                raise HTTPException(
                    status_code=403,
                    detail="Invalid or expired token"
                )

    @staticmethod
    def verify_jwt(jwt_token: str):
        is_token_valid: bool = False
        payload = decode_jwt(jwt_token)
        if payload:
            is_token_valid = True
        return is_token_valid

