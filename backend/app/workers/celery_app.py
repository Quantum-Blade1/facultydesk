from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "facultydesk",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    timezone=settings.TIMEZONE,
    enable_utc=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    beat_schedule={
        "health-check-every-minute": {
            "task": "ping",
            "schedule": 60.0,
        },
    },
)


@celery_app.task(name="ping")
def ping() -> str:
    return "pong"
