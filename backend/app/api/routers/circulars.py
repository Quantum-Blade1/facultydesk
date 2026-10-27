from datetime import date, time
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel

from app.api.deps import get_clock, get_current_principal, get_storage, get_uow
from app.application.circulars.use_cases import (
    ConfirmCircularUseCase,
    GetCircularUseCase,
    ListReviewQueueUseCase,
    RejectCircularUseCase,
    UploadCircularUseCase,
)
from app.application.security.policy import Principal
from app.core.clock import Clock
from app.core.errors import NotFoundError, ValidationError
from app.domain.entities import Circular
from app.domain.repositories import UnitOfWork
from app.infrastructure.storage import StorageService
from app.workers.circular_tasks import process_circular_upload

router = APIRouter(prefix="/circulars", tags=["circulars"])


class CircularUploadResponse(BaseModel):
    id: UUID
    status: str
    file_key: str

    @classmethod
    def from_domain(cls, c: Circular) -> "CircularUploadResponse":
        return cls(
            id=c.id,
            status=c.status.value,
            file_key=c.file_key,
        )


class CircularDetailResponse(BaseModel):
    id: UUID
    file_key: str
    ocr_text: str
    extracted_fields: dict[str, Any]
    confidence: float
    status: str
    failure_reason: str | None

    @classmethod
    def from_domain(cls, c: Circular) -> "CircularDetailResponse":
        return cls(
            id=c.id,
            file_key=c.file_key,
            ocr_text=c.ocr_text,
            extracted_fields=c.extracted_fields,
            confidence=c.confidence,
            status=c.status.value,
            failure_reason=c.failure_reason,
        )


class ConfirmCircularRequest(BaseModel):
    title: str | None = None
    meeting_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    venue: str | None = None
    attendee_ids: list[UUID] | None = None


class ConfirmCircularResponse(BaseModel):
    event_id: UUID
    circular_id: UUID
    status: str


class RejectCircularRequest(BaseModel):
    reason: str = ""


@router.post("/upload", response_model=CircularUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_circular(
    file: UploadFile = File(...),
    department_id: UUID = Form(...),
    auto_confirm: bool = Form(False),
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    storage: StorageService = Depends(get_storage),
) -> CircularUploadResponse:
    """Upload a circular image or PDF for OCR parsing and human review."""
    content = await file.read()
    filename = file.filename or "circular.pdf"
    use_case = UploadCircularUseCase(uow, storage)
    circular = await use_case.execute(
        principal=principal,
        department_id=department_id,
        file_bytes=content,
        filename=filename,
    )
    process_circular_upload.delay(str(circular.id), auto_confirm)
    return CircularUploadResponse.from_domain(circular)


@router.get("/review-queue", response_model=list[CircularDetailResponse])
async def list_review_queue(
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> list[CircularDetailResponse]:
    """List all circulars currently awaiting human review."""
    queue = await ListReviewQueueUseCase(uow).execute()
    return [CircularDetailResponse.from_domain(c) for c in queue]


@router.get("/{circular_id}", response_model=CircularDetailResponse)
async def get_circular(
    circular_id: UUID,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> CircularDetailResponse:
    """Retrieve details, OCR text, and extracted fields for a circular."""
    try:
        circular = await GetCircularUseCase(uow).execute(circular_id)
        return CircularDetailResponse.from_domain(circular)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err)) from err


@router.post("/{circular_id}/confirm", response_model=ConfirmCircularResponse)
async def confirm_circular(
    circular_id: UUID,
    body: ConfirmCircularRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> ConfirmCircularResponse:
    """Confirm a circular from review queue, scheduling the meeting and reminder cascade."""
    try:
        use_case = ConfirmCircularUseCase(uow, clock)
        event = await use_case.execute(
            circular_id=circular_id,
            title=body.title,
            meeting_date=body.meeting_date,
            start_time=body.start_time,
            end_time=body.end_time,
            venue=body.venue,
            attendee_ids=body.attendee_ids,
        )
        return ConfirmCircularResponse(
            event_id=event.id,
            circular_id=circular_id,
            status="CONFIRMED",
        )
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err)) from err
    except ValidationError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err


@router.post("/{circular_id}/reject", response_model=CircularDetailResponse)
async def reject_circular(
    circular_id: UUID,
    body: RejectCircularRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> CircularDetailResponse:
    """Reject a circular from review queue with reason."""
    try:
        await RejectCircularUseCase(uow).execute(circular_id, reason=body.reason)
        circular = await GetCircularUseCase(uow).execute(circular_id)
        return CircularDetailResponse.from_domain(circular)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err)) from err
