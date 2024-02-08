from celery import Celery

from settings import RedisSettings, get_settings

_redis_settings = get_settings(RedisSettings)

celery = Celery(
    "tasks",
    broker=f"redis://{_redis_settings.host}:{_redis_settings.port}",
    include=[
        "tasks.tasks",
        # "src.tasks.scheduled",
    ],
)
