import gzip
import io
import os
import subprocess
from datetime import UTC, datetime, timedelta
from typing import Final

import structlog
from minio import Minio

from app.core.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

BACKUP_BUCKET: Final[str] = "backups"
RETENTION_DAYS: Final[int] = 14


class BackupService:
    def __init__(self, client: Minio | None = None) -> None:
        self._client = client or Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self._ensure_bucket()

    def _ensure_bucket(self) -> None:
        if not self._client.bucket_exists(BACKUP_BUCKET):
            self._client.make_bucket(BACKUP_BUCKET)

    def create_backup(self) -> str:
        timestamp_str = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        backup_key = f"facultydesk_backup_{timestamp_str}.sql.gz"

        env = os.environ.copy()
        env["PGPASSWORD"] = settings.POSTGRES_PASSWORD

        dump_cmd = [
            "pg_dump",
            "-h",
            settings.POSTGRES_HOST,
            "-p",
            str(settings.POSTGRES_PORT),
            "-U",
            settings.POSTGRES_USER,
            "-d",
            settings.POSTGRES_DB,
            "--no-owner",
            "--clean",
            "--if-exists",
        ]

        try:
            dump_proc = subprocess.Popen(
                dump_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
            raw_sql, err = dump_proc.communicate()
            if dump_proc.returncode != 0:
                raise RuntimeError(
                    f"pg_dump failed with code {dump_proc.returncode}: {err.decode('utf-8')}"
                )

            compressed_data = gzip.compress(raw_sql)
            compressed_stream = io.BytesIO(compressed_data)

            self._client.put_object(
                bucket_name=BACKUP_BUCKET,
                object_name=backup_key,
                data=compressed_stream,
                length=len(compressed_data),
                content_type="application/gzip",
            )
            logger.info("backup_created_successfully", key=backup_key, bytes=len(compressed_data))

            self.prune_expired_backups()
            return backup_key
        except Exception as e:
            logger.error("backup_failed", error=str(e))
            raise

    def prune_expired_backups(self) -> int:
        now_utc = datetime.now(UTC)
        cutoff_utc = now_utc - timedelta(days=RETENTION_DAYS)

        objects = list(self._client.list_objects(BACKUP_BUCKET))
        if len(objects) <= 1:
            return 0

        pruned_count = 0
        for obj in objects:
            has_expired = obj.last_modified and obj.last_modified < cutoff_utc
            can_prune = len(objects) - pruned_count > 1
            if has_expired and can_prune:
                self._client.remove_object(BACKUP_BUCKET, obj.object_name)
                pruned_count += 1
                logger.info(
                    "backup_pruned",
                    key=obj.object_name,
                    age_days=(now_utc - obj.last_modified).days,
                )

        return pruned_count

    def restore_backup(self, backup_key: str | None = None) -> None:
        if backup_key is None:
            objects = list(self._client.list_objects(BACKUP_BUCKET))
            if not objects:
                raise RuntimeError("No backups found in storage bucket")
            latest_obj = max(
                objects, key=lambda o: o.last_modified or datetime.min.replace(tzinfo=UTC)
            )
            backup_key = latest_obj.object_name

        resp = self._client.get_object(BACKUP_BUCKET, backup_key)
        try:
            compressed_bytes = resp.read()
            sql_bytes = gzip.decompress(compressed_bytes)
        finally:
            resp.close()
            resp.release_conn()

        env = os.environ.copy()
        env["PGPASSWORD"] = settings.POSTGRES_PASSWORD

        psql_cmd = [
            "psql",
            "-h",
            settings.POSTGRES_HOST,
            "-p",
            str(settings.POSTGRES_PORT),
            "-U",
            settings.POSTGRES_USER,
            "-d",
            settings.POSTGRES_DB,
        ]

        proc = subprocess.run(
            psql_cmd,
            input=sql_bytes,
            capture_output=True,
            env=env,
            check=True,
        )
        logger.info("backup_restored_successfully", key=backup_key, returncode=proc.returncode)
