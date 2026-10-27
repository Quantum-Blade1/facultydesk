import asyncio
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.application.timetable.parse import ParseTimetableUseCase
from app.core.config import get_settings
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork
from app.infrastructure.storage.minio_storage import get_storage_service
from app.workers.celery_app import celery_app


async def _run_parse(upload_id: UUID) -> dict[str, Any]:
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    uow = SqlAlchemyUnitOfWork(session_factory)
    storage = get_storage_service()
    use_case = ParseTimetableUseCase(uow, storage)
    try:
        return await use_case.execute(upload_id)
    finally:
        await engine.dispose()


@celery_app.task(name="process_timetable_upload")
def process_timetable_upload(upload_id_str: str) -> dict[str, Any]:
    upload_id = UUID(upload_id_str)
    return asyncio.run(_run_parse(upload_id))
