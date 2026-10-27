from functools import lru_cache
from io import BytesIO

from minio import Minio
from minio.error import S3Error

from app.core.config import get_settings


class MinioStorageService:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        secure: bool = False,
    ) -> None:
        self._bucket_name = bucket_name
        self._client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self._ensure_bucket()

    def _ensure_bucket(self) -> None:
        try:
            if not self._client.bucket_exists(self._bucket_name):
                self._client.make_bucket(self._bucket_name)
        except S3Error:
            pass

    def upload_file(
        self,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        self._ensure_bucket()
        stream = BytesIO(data)
        self._client.put_object(
            bucket_name=self._bucket_name,
            object_name=key,
            data=stream,
            length=len(data),
            content_type=content_type,
        )
        return key

    def download_file(self, key: str) -> bytes:
        response = self._client.get_object(self._bucket_name, key)
        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()


@lru_cache
def get_storage_service() -> MinioStorageService:
    settings = get_settings()
    return MinioStorageService(
        endpoint=settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        bucket_name=settings.MINIO_BUCKET_NAME,
        secure=settings.MINIO_SECURE,
    )
