import time
import jwt

from ecommerce_api.settings import JWT_SECRET_KEY, ALGORITHM
from ecommerce_api.errors import Unauthorized

"""
Signing, encoding, decoding and returning JSON Web Token (JWS)
"""


def sign_jwt(user_id: str):
    """
    Returns signed JWT string
    """
    payload = {
        "user_id": user_id,
        "expiry": time.time() + 60*60
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}


def decode_jwt(token: str):
    decode_token = jwt.decode(token, JWT_SECRET_KEY, algorithm=ALGORITHM)
    if decode_token.get("expires") <= time.time():
        raise Unauthorized()
    return decode_token


