import asyncio
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.application.circulars.use_cases import ProcessCircularUseCase
from app.core.clock import SystemClock
from app.core.config import get_settings
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork
from app.infrastructure.storage import MinioStorageService
from app.workers.celery_app import celery_app


async def _run_process_circular(circular_id: UUID, auto_confirm: bool = False) -> None:
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    storage = MinioStorageService(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        bucket_name=settings.MINIO_BUCKET_NAME,
        secure=settings.MINIO_SECURE,
    )
    uow = SqlAlchemyUnitOfWork(session_factory)
    clock = SystemClock()
    use_case = ProcessCircularUseCase(storage)

    try:
        await use_case.execute(circular_id, uow, clock, auto_confirm=auto_confirm)
    finally:
        await engine.dispose()


@celery_app.task(name="process_circular_upload")
def process_circular_upload(circular_id_str: str, auto_confirm: bool = False) -> str:
    asyncio.run(_run_process_circular(UUID(circular_id_str), auto_confirm=auto_confirm))
    return f"Processed circular {circular_id_str}"
