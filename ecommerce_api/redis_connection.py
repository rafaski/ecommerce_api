from redis_om import get_redis_connection
from dotenv import load_dotenv
from os import getenv


load_dotenv()
redis_public_endpoint = getenv("REDIS_PUBLIC_ENDPOINT")
redis_port = getenv("REDIS_PORT")
redis_password = getenv("REDIS_PASSWORD")

redis = get_redis_connection(
    host=redis_public_endpoint,
    port=redis_port,
    password=redis_password,
    decode_responses=True
)