from celery import Celery

from ecommerce_api.settings import REDIS_DATA_URL, REDIS_DB

celery = Celery(
    __name__,
    broker=f"{REDIS_DATA_URL}/{REDIS_DB}",
    backend=f"{REDIS_DATA_URL}/{REDIS_DB}"
)

celery.conf.imports = ""