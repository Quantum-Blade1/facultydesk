import re
from uuid import UUID, uuid4

from app.application.security.policy import AuthorisationPolicy, Principal
from app.core.clock import Clock
from app.core.errors import ConflictError
from app.domain import (
    AuditLog,
    InvariantViolation,
    TimetableUpload,
    TimetableUploadStatus,
    UnitOfWork,
)
from app.infrastructure.storage.minio_storage import MinioStorageService

MAX_UPLOAD_SIZE = 15 * 1024 * 1024


class UploadTimetableUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        storage: MinioStorageService,
        clock: Clock,
    ) -> None:
        self._uow = uow
        self._storage = storage
        self._clock = clock

    async def execute(
        self,
        principal: Principal,
        department_id: UUID,
        academic_term_id: UUID,
        file_bytes: bytes,
        file_name: str,
        content_type: str = "application/octet-stream",
    ) -> UUID:
        AuthorisationPolicy.enforce(
            principal, resource_dept_id=department_id, action="upload_timetable"
        )

        if not file_bytes:
            raise InvariantViolation("Uploaded file cannot be empty")

        if len(file_bytes) > MAX_UPLOAD_SIZE:
            raise InvariantViolation("File size exceeds 15 MB limit")

        async with self._uow:
            dept = await self._uow.departments.get_by_id(department_id)
            if dept is None:
                raise ConflictError(f"Department {department_id} not found")

            term = await self._uow.academic_terms.get_by_id(academic_term_id)
            if term is None:
                raise ConflictError(f"Academic term {academic_term_id} not found")

            sanitized_name = re.sub(r"[^a-zA-Z0-9._-]", "_", file_name)
            upload_id = uuid4()
            file_key = f"timetables/{upload_id}_{sanitized_name}"

            self._storage.upload_file(
                key=file_key,
                data=file_bytes,
                content_type=content_type,
            )

            now_utc = self._clock.now()
            upload = TimetableUpload(
                id=upload_id,
                department_id=department_id,
                academic_term_id=academic_term_id,
                file_key=file_key,
                status=TimetableUploadStatus.UPLOADED,
                parse_report={},
                uploaded_at_utc=now_utc,
            )
            await self._uow.timetable_uploads.save(upload)

            audit = AuditLog(
                id=uuid4(),
                user_id=principal.user_id,
                action="upload_timetable",
                resource_type="timetable_upload",
                resource_id=str(upload_id),
                payload={
                    "file_name": file_name,
                    "file_key": file_key,
                    "file_size": len(file_bytes),
                    "department_id": str(department_id),
                    "academic_term_id": str(academic_term_id),
                },
                timestamp_utc=now_utc,
            )
            await self._uow.audit_logs.save(audit)
            await self._uow.commit()

            return upload_id
