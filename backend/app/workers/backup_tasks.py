import structlog

from app.infrastructure.storage.backup_service import BackupService
from app.workers.celery_app import celery_app

logger = structlog.get_logger(__name__)


@celery_app.task(name="backup_database_to_minio")
def backup_database_to_minio() -> str:
    service = BackupService()
    key = service.create_backup()
    logger.info("nightly_backup_completed", backup_key=key)
    return key
