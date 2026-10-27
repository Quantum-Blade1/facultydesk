import uuid
from typing import Any

import structlog
from celery import Celery
from celery.schedules import crontab
from celery.signals import before_task_publish, task_postrun, task_prerun

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "facultydesk",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.workers.calendar_tasks",
        "app.workers.circular_tasks",
        "app.workers.reminder_tasks",
        "app.workers.task_alerts",
        "app.workers.timetable_tasks",
        "app.workers.backup_tasks",
    ],
)

celery_app.conf.update(
    timezone=settings.TIMEZONE,
    enable_utc=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_soft_time_limit=300,
    task_time_limit=360,
    worker_prefetch_multiplier=1,
    beat_schedule={
        "health-check-every-minute": {
            "task": "ping",
            "schedule": 60.0,
        },
        "nightly-materialise-timetable-events": {
            "task": "materialise_all_timetable_events",
            "schedule": crontab(hour=0, minute=5),
        },
        "dispatch-due-notifications-every-30s": {
            "task": "dispatch_due_notifications",
            "schedule": 30.0,
        },
        "recover-stale-sending-notifications-every-5m": {
            "task": "recover_stale_sending_notifications",
            "schedule": 300.0,
        },
        "schedule-daily-overdue-alerts-hourly": {
            "task": "schedule_daily_overdue_alerts",
            "schedule": crontab(minute=0),
        },
        "schedule-hod-escalation-alerts-hourly": {
            "task": "schedule_hod_escalation_alerts",
            "schedule": crontab(minute=30),
        },
        "nightly-database-backup": {
            "task": "backup_database_to_minio",
            "schedule": crontab(hour=2, minute=0),
        },
    },
)


@before_task_publish.connect
def on_before_task_publish(headers: dict[str, Any] | None = None, **kwargs: Any) -> None:
    if headers is not None:
        ctx = structlog.contextvars.get_contextvars()
        req_id = ctx.get("request_id")
        if req_id:
            headers["request_id"] = req_id


@task_prerun.connect
def on_task_prerun(task: Any = None, **kwargs: Any) -> None:
    structlog.contextvars.clear_contextvars()
    req_id = None
    if (
        task
        and hasattr(task, "request")
        and task.request
        and hasattr(task.request, "headers")
        and task.request.headers
    ):
        req_id = task.request.headers.get("request_id")
    if not req_id:
        req_id = str(uuid.uuid4())
    task_id = task.request.id if task and hasattr(task, "request") else str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=req_id, celery_task_id=task_id)


@task_postrun.connect
def on_task_postrun(**kwargs: Any) -> None:
    structlog.contextvars.clear_contextvars()


@celery_app.task(name="ping")
def ping() -> str:
    return "pong"
