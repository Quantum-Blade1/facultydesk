import asyncio
from datetime import timedelta
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.clock import SystemClock
from app.core.config import get_settings
from app.domain import (
    NotificationChannel,
    NotificationStatus,
    ScheduledNotification,
    TaskStatus,
)
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork
from app.workers.celery_app import celery_app


async def _run_schedule_daily_overdue_alerts() -> int:
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    uow = SqlAlchemyUnitOfWork(session_factory)
    clock = SystemClock()
    now_utc = clock.now()
    tz = ZoneInfo("Asia/Kolkata")
    today_ist = now_utc.astimezone(tz).date()

    count = 0
    try:
        async with uow:
            overdue_tasks = await uow.tasks.list_overdue(now_utc)
            for task in overdue_tasks:
                if task.status == TaskStatus.DONE:
                    continue

                idempotency_key = f"task:{task.id}:overdue:{today_ist.isoformat()}"
                existing = await uow.notifications.get_by_idempotency_key(idempotency_key)
                if existing is not None:
                    continue

                fire_local = tz.fromutc(now_utc).replace(
                    hour=9, minute=0, second=0, microsecond=0
                )
                fire_utc = fire_local.astimezone(ZoneInfo("UTC"))
                scheduled_fire_time = fire_utc if fire_utc > now_utc else now_utc

                notif = ScheduledNotification(
                    id=uuid4(),
                    target_id=task.id,
                    target_kind="TASK",
                    user_id=task.assignee_id,
                    channel=NotificationChannel.EMAIL,
                    fire_at_utc=scheduled_fire_time,
                    idempotency_key=idempotency_key,
                    status=NotificationStatus.PENDING,
                )
                await uow.notifications.save(notif)
                count += 1

            await uow.commit()
            return count
    finally:
        await engine.dispose()


async def _run_schedule_hod_escalations() -> int:
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    uow = SqlAlchemyUnitOfWork(session_factory)
    clock = SystemClock()
    now_utc = clock.now()
    tz = ZoneInfo("Asia/Kolkata")
    today_ist = now_utc.astimezone(tz).date()
    cutoff_24h_utc = now_utc - timedelta(hours=24)

    count = 0
    try:
        async with uow:
            overdue_tasks = await uow.tasks.list_overdue(cutoff_24h_utc)
            escalation_assigners: set[UUID] = set()

            for task in overdue_tasks:
                if task.status == TaskStatus.DONE:
                    continue
                if task.parent_assignment_id is not None or task.assigner_id != task.assignee_id:
                    escalation_assigners.add(task.assigner_id)

            for assigner_id in escalation_assigners:
                idempotency_key = f"escalation:hod:{assigner_id}:{today_ist.isoformat()}"
                existing = await uow.notifications.get_by_idempotency_key(idempotency_key)
                if existing is not None:
                    continue

                fire_local = tz.fromutc(now_utc).replace(
                    hour=9, minute=30, second=0, microsecond=0
                )
                fire_utc = fire_local.astimezone(ZoneInfo("UTC"))
                scheduled_fire = fire_utc if fire_utc > now_utc else now_utc

                notif = ScheduledNotification(
                    id=uuid4(),
                    target_id=assigner_id,
                    target_kind="ESCALATION",
                    user_id=assigner_id,
                    channel=NotificationChannel.EMAIL,
                    fire_at_utc=scheduled_fire,
                    idempotency_key=idempotency_key,
                    status=NotificationStatus.PENDING,
                )
                await uow.notifications.save(notif)
                count += 1

            await uow.commit()
            return count
    finally:
        await engine.dispose()


@celery_app.task(name="schedule_daily_overdue_alerts")
def schedule_daily_overdue_alerts() -> int:
    return asyncio.run(_run_schedule_daily_overdue_alerts())


@celery_app.task(name="schedule_hod_escalation_alerts")
def schedule_hod_escalation_alerts() -> int:
    return asyncio.run(_run_schedule_hod_escalations())
