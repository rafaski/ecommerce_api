import time
import jwt

from ecommerce_api.settings import JWT_SECRET_KEY, ALGORITHM

"""
Signing, encoding, decoding and returning JSON Web Tokens (JWSs)
"""


def token_response(token: str):
    """
    Returns the generated Tokens (JWTs)
    """
    return {
        "access token": token
    }


def sign_jwt(user_id: str):
    """
    Returns signed JWT string
    """
    payload = {
        "user_id": user_id,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token_response(token)


def decode_jwt(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET_KEY, algorithm=ALGORITHM)
        if decode_token.get("expires") <= time.time():
            return None
        return decode_token
    except:
        return {}


