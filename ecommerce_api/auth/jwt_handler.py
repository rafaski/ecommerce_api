import time
import jwt

from ecommerce_api.settings import JWT_SECRET_KEY, ALGORITHM
from ecommerce_api.errors import Unauthorized

"""
Signing, encoding, decoding and returning JSON Web Token (JWS)
"""


def sign_jwt(email: str) -> str:
    """
    Returns signed JWT string
    """
    payload = {
        "email": email,
        "ttl": time.time() + 60*60
    }
    token = jwt.encode(
        payload=payload,
        key=JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token


def decode_jwt(token: str) -> str:
    decode_token = jwt.decode(
        jwt=token,
        key=JWT_SECRET_KEY,
        algorithm=ALGORITHM
    )
    if decode_token.get("ttl") <= time.time():
        raise Unauthorized()
    return decode_token


