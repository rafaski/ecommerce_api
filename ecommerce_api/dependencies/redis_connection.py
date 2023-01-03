from redis_om import get_redis_connection
from os import getenv

redis_public_endpoint = getenv("REDIS_PUBLIC_ENDPOINT")
redis_port = getenv("REDIS_PORT")
redis_password = getenv("REDIS_PASSWORD")

redis_conn = get_redis_connection(
    host=redis_public_endpoint,
    port=redis_port,
    password=redis_password,
    decode_responses=True
)
