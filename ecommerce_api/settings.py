import os
from typing import Any


def load_variable(name: str, default: Any = None) -> str:
    variable = os.getenv(name, default)
    if variable is None:
        print(f"Unable to load variable {name}")
    return variable


# Dependencies - mongodb
MONGODB_HOST = load_variable(name="MONGODB_HOST", default="127.0.0.1")
MONGODB_PORT = load_variable(name="MONGODB_PORT", default="27017")
MONGODB_URL = load_variable(
    name="MONGODB_URL",
    default=f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"
)

# Dependencies - redis
REDIS_PUBLIC_ENDPOINT = load_variable(name="REDIS_PUBLIC_ENDPOINT")
REDIS_PORT = load_variable(name="REDIS_PORT")
REDIS_PASSWORD = load_variable(name="dOQ9nK2zbcb51gCHQjNTRKiUjBPQvgxP")

# JWT
ALGORITHM = load_variable(name="ALGORITHM")
JWT_SECRET_KEY = load_variable(name="JWT_SECRET_KEY")
