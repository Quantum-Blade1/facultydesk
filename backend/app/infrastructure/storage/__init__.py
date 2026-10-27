from app.infrastructure.storage.minio_storage import MinioStorageService, get_storage_service

StorageService = MinioStorageService

__all__ = ["MinioStorageService", "StorageService", "get_storage_service"]
