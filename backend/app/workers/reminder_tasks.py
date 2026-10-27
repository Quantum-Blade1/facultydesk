import asyncio

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.application.reminders.dispatcher import ReminderDispatcher
from app.core.clock import SystemClock
from app.core.config import get_settings
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork
from app.infrastructure.notifiers import CompositeNotifier, EmailNotifier, WebPushNotifier
from app.workers.celery_app import celery_app


def _build_dispatcher() -> tuple[ReminderDispatcher, async_sessionmaker[AsyncSession], AsyncEngine]:
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    email_notifier = EmailNotifier(
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        sender=settings.SMTP_FROM,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
    )
    push_notifier = WebPushNotifier(
        vapid_private_key=settings.VAPID_PRIVATE_KEY,
        vapid_claims_email=settings.VAPID_CLAIMS_EMAIL,
    )
    composite = CompositeNotifier(email_notifier, push_notifier)
    dispatcher = ReminderDispatcher(
        clock=SystemClock(),
        notifier=composite,
        app_url="http://localhost:3000",
    )
    return dispatcher, session_factory, engine


async def _run_dispatch(batch_size: int = 100) -> int:
    dispatcher, session_factory, engine = _build_dispatcher()
    uow = SqlAlchemyUnitOfWork(session_factory)
    try:
        return await dispatcher.dispatch_due(uow, batch_size=batch_size)
    finally:
        await engine.dispose()


async def _run_recover(stale_minutes: int = 5) -> int:
    dispatcher, session_factory, engine = _build_dispatcher()
    uow = SqlAlchemyUnitOfWork(session_factory)
    try:
        return await dispatcher.recover_stale_sending(uow, stale_minutes=stale_minutes)
    finally:
        await engine.dispose()


@celery_app.task(name="dispatch_due_notifications")
def dispatch_due_notifications() -> int:
    return asyncio.run(_run_dispatch(100))


@celery_app.task(name="recover_stale_sending_notifications")
def recover_stale_sending_notifications() -> int:
    return asyncio.run(_run_recover(5))
