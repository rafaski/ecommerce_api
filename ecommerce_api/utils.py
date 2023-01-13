from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_string(user_input: str) -> str:
    """
    String hashing
    """
    return crypt_context.hash(secret=user_input)


def compare_hashed_string(original_string: str, hashed_string: str) -> bool:
    """
    Verifying user password
    """
    is_valid = crypt_context.verify(
        secret=original_string,
        hash=hashed_string
    )
    return is_valid
