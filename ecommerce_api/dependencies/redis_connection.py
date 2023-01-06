from aredis_om import get_redis_connection, Migrator

from ecommerce_api.settings import (
    REDIS_PORT, REDIS_PASSWORD, REDIS_URL
)


redis_connection = get_redis_connection(
    host=REDIS_URL,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

Migrator(redis_connection).run()
