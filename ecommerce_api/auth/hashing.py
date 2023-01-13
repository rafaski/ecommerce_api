from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifying user password
    """
    is_valid = pwd_context.verify(password, hashed_password)
    return is_valid


def hash_password(password: str) -> str:
    """
    Hashing user password
    """
    hashed_password = pwd_context.hash(password)
    return hashed_password
