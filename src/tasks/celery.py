from celery import Celery

from settings import redis_settings

celery = Celery(
    "tasks",
    broker=f"redis://{redis_settings.HOST}:{redis_settings.PORT}",
    include=[
        "tasks.tasks",
        # "src.tasks.scheduled",
    ],
)
