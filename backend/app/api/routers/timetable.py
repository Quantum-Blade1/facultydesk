from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from pydantic import BaseModel

from app.api.deps import (
    get_clock,
    get_current_principal,
    get_storage,
    get_uow,
    require_hod_or_admin,
)
from app.application.security.policy import AuthorisationPolicy, Principal
from app.application.timetable.confirm import ConfirmTimetableUseCase
from app.application.timetable.parse import ParseTimetableUseCase
from app.application.timetable.upload import UploadTimetableUseCase
from app.core.clock import Clock
from app.core.errors import NotFoundError
from app.domain import UnitOfWork
from app.infrastructure.storage.minio_storage import MinioStorageService
from app.workers.timetable_tasks import process_timetable_upload

router = APIRouter(prefix="/timetables", tags=["timetables"])


class UploadTimetableResponse(BaseModel):
    upload_id: UUID
    status: str
    message: str


class TimetableUploadDetailResponse(BaseModel):
    id: UUID
    department_id: UUID
    academic_term_id: UUID
    status: str
    parse_report: dict[str, Any]
    uploaded_at_utc: str


class ConfirmTimetableResponse(BaseModel):
    upload_id: UUID
    slots_created: int
    status: str


class TimetableSlotResponse(BaseModel):
    id: UUID
    timetable_upload_id: UUID
    weekday: int
    start_time: str
    end_time: str
    course_id: UUID
    section_id: UUID
    room_id: UUID
    faculty_id: UUID
    source_cell_reference: str


@router.post(
    "/upload",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UploadTimetableResponse,
)
async def upload_timetable(
    department_id: UUID = Form(...),
    academic_term_id: UUID = Form(...),
    file: UploadFile = File(...),
    principal: Principal = Depends(require_hod_or_admin),
    uow: UnitOfWork = Depends(get_uow),
    storage: MinioStorageService = Depends(get_storage),
    clock: Clock = Depends(get_clock),
) -> UploadTimetableResponse:
    """Upload a timetable file for parsing and initials resolution."""
    content = await file.read()
    use_case = UploadTimetableUseCase(uow, storage, clock)
    upload_id = await use_case.execute(
        principal=principal,
        department_id=department_id,
        academic_term_id=academic_term_id,
        file_bytes=content,
        file_name=file.filename or "timetable.xlsx",
        content_type=file.content_type or "application/octet-stream",
    )

    try:
        process_timetable_upload.delay(str(upload_id))
    except Exception:
        parse_uc = ParseTimetableUseCase(uow, storage)
        await parse_uc.execute(upload_id)

    return UploadTimetableResponse(
        upload_id=upload_id,
        status="UPLOADED",
        message="Timetable uploaded and parsing initiated",
    )


@router.get(
    "/{upload_id}",
    response_model=TimetableUploadDetailResponse,
)
async def get_timetable_upload(
    upload_id: UUID,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> TimetableUploadDetailResponse:
    """Retrieve status, preview slots, and unresolved tokens for a timetable upload."""
    async with uow:
        upload = await uow.timetable_uploads.get_by_id(upload_id)
        if upload is None:
            raise NotFoundError(f"Timetable upload {upload_id} not found")

        AuthorisationPolicy.enforce(
            principal,
            resource_dept_id=upload.department_id,
            action="read_timetable",
        )

        return TimetableUploadDetailResponse(
            id=upload.id,
            department_id=upload.department_id,
            academic_term_id=upload.academic_term_id,
            status=upload.status.value,
            parse_report=upload.parse_report,
            uploaded_at_utc=upload.uploaded_at_utc.isoformat(),
        )


@router.post(
    "/{upload_id}/confirm",
    status_code=status.HTTP_200_OK,
    response_model=ConfirmTimetableResponse,
)
async def confirm_timetable(
    upload_id: UUID,
    principal: Principal = Depends(require_hod_or_admin),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> ConfirmTimetableResponse:
    """Confirm a previewed timetable upload, generating courses, sections and slots."""
    use_case = ConfirmTimetableUseCase(uow, clock)
    slots_created, _ = await use_case.execute(principal, upload_id)
    return ConfirmTimetableResponse(
        upload_id=upload_id,
        slots_created=slots_created,
        status="CONFIRMED",
    )


@router.get(
    "/faculty/{faculty_id}",
    response_model=list[TimetableSlotResponse],
)
async def get_faculty_slots(
    faculty_id: UUID,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> list[TimetableSlotResponse]:
    """Retrieve all confirmed timetable slots assigned to a specific faculty profile."""
    async with uow:
        profile = await uow.faculty_profiles.get_by_id(faculty_id)
        if profile is None:
            raise NotFoundError(f"Faculty profile {faculty_id} not found")

        AuthorisationPolicy.enforce(
            principal,
            resource_owner_id=profile.user_id,
            resource_dept_id=profile.department_id,
            action="read_timetable_slots",
        )

        slots = await uow.timetable_slots.list_by_faculty_id(faculty_id)
        return [
            TimetableSlotResponse(
                id=s.id,
                timetable_upload_id=s.timetable_upload_id,
                weekday=s.time_slot.weekday,
                start_time=s.time_slot.start_time.isoformat(),
                end_time=s.time_slot.end_time.isoformat(),
                course_id=s.course_id,
                section_id=s.section_id,
                room_id=s.room_id,
                faculty_id=s.faculty_id,
                source_cell_reference=s.source_cell_reference,
            )
            for s in slots
        ]
