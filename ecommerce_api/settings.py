import os
from typing import Any
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()


@lru_cache()
def load_variable(name: str, default: Any = None) -> str:
    variable = os.getenv(name, default)
    if variable is None:
        print(f"Unable to load variable {name}")
    return variable


# Dependencies - redis
REDIS_HOST = load_variable(name="REDIS_HOST", default="127.0.0.1")
REDIS_DATA_PORT = load_variable(name="REDIS_PORT", default="6379")
REDIS_DATA_URL = load_variable(
    name="REDIS_URL",
    default=f"redis://{REDIS_HOST}:{REDIS_DATA_PORT}"
)
REDIS_DB = load_variable(name="REDIS_DB", default="0")
REDIS_CACHE_PORT = load_variable(name="REDIS_PORT", default="6381")
REDIS_CACHE_URL = load_variable(
    name="REDIS_URL",
    default=f"redis://{REDIS_HOST}:{REDIS_CACHE_PORT}"
)

# DB
DATABASE_URL = load_variable(
    name="DATABASE_URL",
    default="sqlite:///./sql_app.db"
)

# JWT
ALGORITHM = load_variable(name="ALGORITHM")
JWT_SECRET_KEY = load_variable(name="JWT_SECRET_KEY")

# slack
SLACK_WEBHOOK_URL = load_variable(name="SLACK_WEBHOOK_URL")

# celery
CELERY_BROKER_URL = load_variable(name="CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = load_variable(name="CELERY_RESULT_BACKEND")



