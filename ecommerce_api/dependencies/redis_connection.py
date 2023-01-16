import redis

from ecommerce_api.settings import REDIS_CACHE_URL, REDIS_DATA_URL

# redis data
redis_connection = redis.asyncio.from_url(
    url=REDIS_DATA_URL,
    decode_responses=True
)


# redis cache
redis_cache = redis.asyncio.from_url(
    url=REDIS_CACHE_URL,
    encoding="utf8",
    decode_responses=True
)
