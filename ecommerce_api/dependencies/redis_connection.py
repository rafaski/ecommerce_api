from aredis_om import get_redis_connection, Migrator
from redis import asyncio

from ecommerce_api.settings import REDIS_CACHE_URL, REDIS_DATA_URL

# redis data
redis_connection = get_redis_connection(
    url=REDIS_DATA_URL,
    decode_responses=True
)

Migrator().run()

# redis cache
redis_cache = asyncio.from_url(
    REDIS_CACHE_URL,
    encoding="utf8",
    decode_responses=True
)
