from datetime import UTC, date, datetime, time, timedelta
from typing import Any
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from app.application.calendar.use_cases import CreateEventUseCase
from app.application.security.policy import Principal
from app.core.clock import Clock
from app.core.errors import NotFoundError, ValidationError
from app.core.upload_guard import validate_upload_content
from app.domain.entities import Circular, Event
from app.domain.repositories import UnitOfWork
from app.domain.value_objects import CircularStatus, EventKind, EventSource
from app.infrastructure.ocr.duplicate_detector import detect_probable_duplicate
from app.infrastructure.ocr.engine import OcrEngine
from app.infrastructure.ocr.extractor import CircularExtractor
from app.infrastructure.ocr.preprocessor import (
    has_pdf_text_layer,
    preprocess_image_for_ocr,
    rasterise_pdf_page,
)
from app.infrastructure.storage import StorageService

ALLOWED_CIRCULAR_MIMES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
}


class UploadCircularUseCase:
    def __init__(self, uow: UnitOfWork, storage: StorageService) -> None:
        self._uow = uow
        self._storage = storage

    async def execute(
        self,
        principal: Principal,
        department_id: UUID,
        file_bytes: bytes,
        filename: str,
    ) -> Circular:
        mime, ext = validate_upload_content(
            file_bytes,
            allowed_mimes={"application/pdf", "image/png", "image/jpeg"},
        )

        circular_id = uuid4()
        key = f"circulars/{department_id}/{circular_id}{ext}"
        self._storage.upload_file(key, file_bytes, mime)

        circular = Circular(
            id=circular_id,
            file_key=key,
            status=CircularStatus.UPLOADED,
            extracted_fields={"department_id": str(department_id), "filename": filename},
        )
        return await self._uow.circulars.save(circular)


class ProcessCircularUseCase:
    def __init__(
        self,
        storage: StorageService,
        ocr_engine: OcrEngine | None = None,
        extractor: CircularExtractor | None = None,
    ) -> None:
        self._storage = storage
        self._ocr = ocr_engine or OcrEngine(confidence_threshold=70.0)
        self._extractor = extractor or CircularExtractor()

    async def execute(
        self,
        circular_id: UUID,
        uow: UnitOfWork,
        clock: Clock,
        auto_confirm: bool = False,
    ) -> Circular:
        circular = await uow.circulars.get_by_id(circular_id)
        if circular is None:
            raise NotFoundError(f"Circular '{circular_id}' was not found")

        circular.start_processing()
        await uow.circulars.save(circular)
        await uow.commit()

        try:
            file_bytes = self._storage.download_file(circular.file_key)
            extracted_text = ""
            doc_confidence = 0.0

            is_pdf = circular.file_key.endswith(".pdf") or file_bytes.startswith(b"%PDF")
            if is_pdf:
                has_text, text_content = has_pdf_text_layer(file_bytes)
                if has_text:
                    extracted_text = text_content
                    doc_confidence = 100.0
                else:
                    raster_bytes = rasterise_pdf_page(file_bytes, page_index=0, dpi=300)
                    processed_img, _ = preprocess_image_for_ocr(raster_bytes)
                    ocr_res = self._ocr.extract_text(processed_img)
                    extracted_text = ocr_res.text
                    doc_confidence = ocr_res.confidence
            else:
                processed_img, _ = preprocess_image_for_ocr(file_bytes)
                ocr_res = self._ocr.extract_text(processed_img)
                extracted_text = ocr_res.text
                doc_confidence = ocr_res.confidence

            dept_id_str = circular.extracted_fields.get("department_id")
            dept_id = UUID(dept_id_str) if dept_id_str else None
            faculty_profiles = (
                await uow.faculty_profiles.list_by_department(dept_id) if dept_id else []
            )

            is_probable_dup = False
            probable_dup_id: UUID | None = None
            temp_res = self._extractor.extract(extracted_text, doc_confidence, faculty_profiles)

            if temp_res.meeting_date and temp_res.extracted_time:
                tz = ZoneInfo("Asia/Kolkata")
                day_start_utc = (
                    datetime.combine(temp_res.meeting_date, time.min)
                    .replace(tzinfo=tz)
                    .astimezone(UTC)
                )
                day_end_utc = day_start_utc + timedelta(days=1)
                day_events = await uow.events.list_by_faculty_and_range(
                    faculty_profiles[0].id if faculty_profiles else uuid4(),
                    day_start_utc,
                    day_end_utc,
                )
                is_probable_dup, probable_dup_id = detect_probable_duplicate(
                    candidate_title=temp_res.title,
                    candidate_date=temp_res.meeting_date,
                    candidate_start_time=temp_res.extracted_time.start_time,
                    existing_events=day_events,
                )

            extraction = self._extractor.extract(
                text=extracted_text,
                document_confidence=doc_confidence,
                faculty_profiles=faculty_profiles,
                is_probable_duplicate=is_probable_dup,
            )

            extracted_fields: dict[str, Any] = {
                "department_id": str(dept_id) if dept_id else None,
                "title": extraction.title,
                "agenda": extraction.agenda,
                "date": (extraction.meeting_date.isoformat() if extraction.meeting_date else None),
                "date_confidence": extraction.date_confidence,
                "start_time": (
                    extraction.extracted_time.start_time.strftime("%H:%M")
                    if extraction.extracted_time
                    else None
                ),
                "end_time": (
                    extraction.extracted_time.end_time.strftime("%H:%M")
                    if extraction.extracted_time
                    else None
                ),
                "time_confidence": (
                    extraction.extracted_time.confidence if extraction.extracted_time else 0.0
                ),
                "is_duration_assumed": (
                    extraction.extracted_time.is_assumed_duration
                    if extraction.extracted_time
                    else False
                ),
                "venue": extraction.venue,
                "venue_confidence": extraction.venue_confidence,
                "is_all_faculty": extraction.is_all_faculty,
                "attendees": [
                    {
                        "faculty_id": str(a.faculty_id),
                        "full_name": a.full_name,
                        "initials": a.initials,
                        "confidence": a.confidence,
                        "match_type": a.match_type,
                    }
                    for a in extraction.attendees
                ],
                "review_reasons": extraction.review_reasons,
                "probable_duplicate_event_id": (str(probable_dup_id) if probable_dup_id else None),
            }

            circular.ocr_text = extracted_text
            circular.confidence = doc_confidence

            if extraction.is_auto_confirmable and auto_confirm:
                tz = ZoneInfo("Asia/Kolkata")
                assert extraction.meeting_date is not None
                assert extraction.extracted_time is not None
                start_dt = (
                    datetime.combine(extraction.meeting_date, extraction.extracted_time.start_time)
                    .replace(tzinfo=tz)
                    .astimezone(UTC)
                )
                end_dt = (
                    datetime.combine(extraction.meeting_date, extraction.extracted_time.end_time)
                    .replace(tzinfo=tz)
                    .astimezone(UTC)
                )

                create_event_uc = CreateEventUseCase(uow, clock)
                created_event = await create_event_uc.execute(
                    kind=EventKind.MEETING,
                    title=extraction.title,
                    start_utc=start_dt,
                    end_utc=end_dt,
                    location=extraction.venue,
                    attendee_ids=[a.faculty_id for a in extraction.attendees],
                    override_clashes=True,
                    source=EventSource.CIRCULAR,
                )
                extracted_fields["event_id"] = str(created_event.id)
                circular.confirm(extracted_fields)
            else:
                circular.mark_needs_review(extracted_fields, doc_confidence)

            await uow.circulars.save(circular)
            await uow.commit()
            return circular

        except Exception as exc:
            circular.fail(str(exc))
            await uow.circulars.save(circular)
            await uow.commit()
            raise


class GetCircularUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, circular_id: UUID) -> Circular:
        c = await self._uow.circulars.get_by_id(circular_id)
        if c is None:
            raise NotFoundError(f"Circular '{circular_id}' was not found")
        return c


class ListReviewQueueUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self) -> list[Circular]:
        return await self._uow.circulars.list_pending_review()


class ConfirmCircularUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        circular_id: UUID,
        title: str | None = None,
        meeting_date: date | None = None,
        start_time: time | None = None,
        end_time: time | None = None,
        venue: str | None = None,
        attendee_ids: list[UUID] | None = None,
    ) -> Event:
        circular = await self._uow.circulars.get_by_id(circular_id)
        if circular is None:
            raise NotFoundError(f"Circular '{circular_id}' was not found")

        fields = dict(circular.extracted_fields)
        tz = ZoneInfo("Asia/Kolkata")

        final_title = title or str(fields.get("title", "Department Meeting"))
        final_venue = venue or str(fields.get("venue", "Department Meeting Room"))

        if meeting_date is None:
            raw_d = fields.get("date")
            if not raw_d:
                raise ValidationError("Cannot confirm meeting without a valid date")
            final_date = date.fromisoformat(str(raw_d))
        else:
            final_date = meeting_date

        if start_time is None:
            raw_st = fields.get("start_time")
            if not raw_st:
                raise ValidationError("Cannot confirm meeting without a valid start time")
            h, m = map(int, str(raw_st).split(":"))
            final_start = time(h, m)
        else:
            final_start = start_time

        if end_time is None:
            raw_et = fields.get("end_time")
            if raw_et:
                h, m = map(int, str(raw_et).split(":"))
                final_end = time(h, m)
            else:
                final_end = time((final_start.hour + 1) % 24, final_start.minute)
        else:
            final_end = end_time

        if attendee_ids is None:
            raw_att = fields.get("attendees", [])
            final_attendee_ids = [UUID(a["faculty_id"]) for a in raw_att]
        else:
            final_attendee_ids = attendee_ids

        start_dt = datetime.combine(final_date, final_start).replace(tzinfo=tz).astimezone(UTC)
        end_dt = datetime.combine(final_date, final_end).replace(tzinfo=tz).astimezone(UTC)
        if end_dt <= start_dt:
            end_dt += timedelta(days=1)

        create_uc = CreateEventUseCase(self._uow, self._clock)
        event = await create_uc.execute(
            kind=EventKind.MEETING,
            title=final_title,
            start_utc=start_dt,
            end_utc=end_dt,
            location=final_venue,
            attendee_ids=final_attendee_ids,
            override_clashes=True,
            source=EventSource.CIRCULAR,
        )

        fields["event_id"] = str(event.id)
        circular.confirm(fields)
        await self._uow.circulars.save(circular)
        return event


class RejectCircularUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, circular_id: UUID, reason: str = "") -> None:
        circular = await self._uow.circulars.get_by_id(circular_id)
        if circular is None:
            raise NotFoundError(f"Circular '{circular_id}' was not found")

        circular.reject(reason)
        await self._uow.circulars.save(circular)
