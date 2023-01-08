from aredis_om import get_redis_connection, Migrator

from ecommerce_api.settings import REDIS_URL


redis_connection = get_redis_connection(
    url=REDIS_URL,
    decode_responses=True
)

Migrator().run()
