import asyncio
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.application.calendar.use_cases import MaterialiseTimetableEventsUseCase
from app.core.clock import SystemClock
from app.core.config import get_settings
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork
from app.workers.celery_app import celery_app


async def _run_materialisation(upload_id: UUID | None = None) -> int:
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    uow = SqlAlchemyUnitOfWork(session_factory)
    clock = SystemClock()
    use_case = MaterialiseTimetableEventsUseCase(uow, clock)
    try:
        async with uow:
            count = await use_case.execute(upload_id)
            await uow.commit()
            return count
    finally:
        await engine.dispose()


@celery_app.task(name="materialise_all_timetable_events")
def materialise_all_timetable_events() -> int:
    return asyncio.run(_run_materialisation(None))


@celery_app.task(name="materialise_timetable_upload")
def materialise_timetable_upload(upload_id_str: str) -> int:
    upload_id = UUID(upload_id_str)
    return asyncio.run(_run_materialisation(upload_id))
