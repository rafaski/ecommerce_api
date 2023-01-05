from redis_om import get_redis_connection

from ecommerce_api.settings import (
    REDIS_PORT, REDIS_PASSWORD, REDIS_PUBLIC_ENDPOINT
)


redis_conn = get_redis_connection(
    host=REDIS_PUBLIC_ENDPOINT,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)
