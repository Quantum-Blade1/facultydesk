from datetime import date, datetime, time
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, Field

from app.api.deps import get_clock, get_current_principal, get_uow
from app.application.calendar.use_cases import (
    CancelEventUseCase,
    CheckClashesUseCase,
    CreateEventUseCase,
    FindFreeSlotsUseCase,
    GenerateIcsFeedUseCase,
    GetCalendarEventsUseCase,
    RotateIcsTokenUseCase,
    UpdateEventUseCase,
)
from app.application.security.policy import Principal
from app.core.clock import Clock
from app.core.errors import ForbiddenError, NotFoundError, ValidationError
from app.domain.entities import Event
from app.domain.errors import ClashDetectedError, EntityNotFound
from app.domain.repositories import UnitOfWork
from app.domain.value_objects import EventKind, EventSource, Role

router = APIRouter(prefix="/calendar", tags=["calendar"])


class EventAttendeeResponse(BaseModel):
    id: UUID
    faculty_id: UUID
    response: str


class CalendarEventResponse(BaseModel):
    id: UUID
    kind: str
    title: str
    start_utc: str
    end_utc: str
    location: str
    source: str
    source_id: UUID | None
    recurrence_date: str | None
    attendees: list[EventAttendeeResponse]

    @classmethod
    def from_domain(cls, event: Event) -> "CalendarEventResponse":
        return cls(
            id=event.id,
            kind=event.kind.value,
            title=event.title,
            start_utc=event.start_utc.isoformat(),
            end_utc=event.end_utc.isoformat(),
            location=event.location,
            source=event.source.value,
            source_id=event.source_id,
            recurrence_date=event.recurrence_date.isoformat() if event.recurrence_date else None,
            attendees=[
                EventAttendeeResponse(
                    id=att.id,
                    faculty_id=att.faculty_id,
                    response=att.response.value,
                )
                for att in event.attendees
            ],
        )


class CreateEventRequest(BaseModel):
    kind: EventKind = EventKind.CUSTOM
    title: str

    start_utc: datetime
    end_utc: datetime
    location: str = ""
    attendee_ids: list[UUID] = Field(default_factory=list)
    override_clashes: bool = False


class UpdateEventRequest(BaseModel):
    title: str | None = None
    location: str | None = None
    start_utc: datetime | None = None
    end_utc: datetime | None = None
    attendee_ids: list[UUID] | None = None
    override_clashes: bool = False


class CheckClashesRequest(BaseModel):
    start_utc: datetime
    end_utc: datetime
    attendee_ids: list[UUID]
    exclude_event_id: UUID | None = None


class FindFreeSlotsRequest(BaseModel):
    attendee_ids: list[UUID]
    start_date: date
    end_date: date
    duration_minutes: int = 60
    work_start_time: time = time(8, 0)
    work_end_time: time = time(18, 0)


class FreeSlotResponse(BaseModel):
    start_utc: str
    end_utc: str


@router.get("/events", response_model=list[CalendarEventResponse])
async def list_calendar_events(
    start: datetime = Query(...),
    end: datetime = Query(...),
    faculty_id: UUID | None = Query(None),
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> list[CalendarEventResponse]:
    """Retrieve calendar events for a faculty member within a half-open interval."""
    async with uow:
        target_fid = faculty_id
        if target_fid is None:
            profile = await uow.faculty_profiles.get_by_user_id(principal.user_id)
            if profile is None:
                msg = f"FacultyProfile with user_id '{principal.user_id}' was not found"
                raise NotFoundError(msg)
            target_fid = profile.id

        else:
            if principal.role == Role.FACULTY:
                profile = await uow.faculty_profiles.get_by_user_id(principal.user_id)
                if profile is None or profile.id != target_fid:
                    raise ForbiddenError("Faculty can only view their own calendar")
            elif principal.role == Role.HOD:
                profile = await uow.faculty_profiles.get_by_id(target_fid)
                if profile is None or profile.department_id != principal.department_id:
                    raise ForbiddenError("HOD can only view departmental faculty calendars")

        use_case = GetCalendarEventsUseCase(uow)
        events = await use_case.execute(target_fid, start, end)
        return [CalendarEventResponse.from_domain(ev) for ev in events]


@router.post(
    "/events",
    response_model=CalendarEventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_calendar_event(
    req: CreateEventRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> CalendarEventResponse:
    """Create a manual event or meeting with clash detection."""
    async with uow:
        profile = await uow.faculty_profiles.get_by_user_id(principal.user_id)
        if profile is None and principal.role == Role.FACULTY:
            raise NotFoundError(f"FacultyProfile with user_id '{principal.user_id}' was not found")

        attendee_ids = req.attendee_ids
        if not attendee_ids:
            if profile is not None:
                attendee_ids = [profile.id]
            else:
                raise ValidationError("attendee_ids must be specified")

        if principal.role == Role.FACULTY and (profile is None or attendee_ids != [profile.id]):
            raise ForbiddenError("Faculty can only create personal calendar events")

        use_case = CreateEventUseCase(uow, clock)
        try:
            event = await use_case.execute(
                kind=req.kind,
                title=req.title,
                start_utc=req.start_utc,
                end_utc=req.end_utc,
                location=req.location,
                attendee_ids=attendee_ids,
                override_clashes=req.override_clashes,
                source=EventSource.MANUAL,
            )
            await uow.commit()
            return CalendarEventResponse.from_domain(event)
        except ClashDetectedError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": str(e), "clashes": e.clashes},
            ) from e


@router.put("/events/{event_id}", response_model=CalendarEventResponse)
async def update_calendar_event(
    event_id: UUID,
    req: UpdateEventRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> CalendarEventResponse:
    """Update or reschedule an event with clash detection."""
    async with uow:
        event = await uow.events.get_by_id(event_id)
        if event is None:
            raise NotFoundError(f"Event with id '{event_id}' was not found")

        if principal.role == Role.FACULTY:
            profile = await uow.faculty_profiles.get_by_user_id(principal.user_id)
            if profile is None or not any(att.faculty_id == profile.id for att in event.attendees):
                raise ForbiddenError("Faculty can only update events on their calendar")

        use_case = UpdateEventUseCase(uow, clock)
        try:
            updated = await use_case.execute(
                event_id=event_id,
                title=req.title,
                location=req.location,
                start_utc=req.start_utc,
                end_utc=req.end_utc,
                attendee_ids=req.attendee_ids,
                override_clashes=req.override_clashes,
            )
            await uow.commit()
            return CalendarEventResponse.from_domain(updated)
        except ClashDetectedError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": str(e), "clashes": e.clashes},
            ) from e


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_calendar_event(
    event_id: UUID,
    reason: str = Query("", description="Cancellation reason"),
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> None:
    """Cancel and delete an event from the calendar."""
    async with uow:
        event = await uow.events.get_by_id(event_id)
        if event is None:
            raise NotFoundError(f"Event with id '{event_id}' was not found")

        if principal.role == Role.FACULTY:
            profile = await uow.faculty_profiles.get_by_user_id(principal.user_id)
            if profile is None or not any(att.faculty_id == profile.id for att in event.attendees):
                raise ForbiddenError("Faculty can only cancel events on their calendar")

        use_case = CancelEventUseCase(uow, clock)
        await use_case.execute(event_id=event_id, reason=reason)
        await uow.commit()


@router.post("/clashes")
async def check_event_clashes(
    req: CheckClashesRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> dict[str, Any]:
    """Dry-run check to identify potential timetable or event clashes."""
    async with uow:
        use_case = CheckClashesUseCase(uow)
        clashes = await use_case.execute(
            start_utc=req.start_utc,
            end_utc=req.end_utc,
            attendee_ids=req.attendee_ids,
            exclude_event_id=req.exclude_event_id,
        )
        return {"clashes": clashes, "has_clashes": len(clashes) > 0}


@router.post("/free-slots", response_model=list[FreeSlotResponse])
async def find_common_free_slots(
    req: FindFreeSlotsRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> list[FreeSlotResponse]:
    """Find mutual free intervals among attendees across a date range."""
    async with uow:
        use_case = FindFreeSlotsUseCase(uow)
        slots = await use_case.execute(
            attendee_ids=req.attendee_ids,
            start_date=req.start_date,
            end_date=req.end_date,
            duration_minutes=req.duration_minutes,
            work_start_time=req.work_start_time,
            work_end_time=req.work_end_time,
        )
        return [
            FreeSlotResponse(
                start_utc=s.isoformat(),
                end_utc=e.isoformat(),
            )
            for s, e in slots
        ]


@router.get("/ics/{feed_token}.ics")
async def get_ics_feed(
    feed_token: str,
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> Response:
    """Public token-gated endpoint serving an RFC 5545 iCalendar feed."""
    async with uow:
        use_case = GenerateIcsFeedUseCase(uow, clock)
        try:
            filename, ics_bytes = await use_case.execute(feed_token)
        except EntityNotFound as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Calendar feed token not found",
            ) from e

        return Response(
            content=ics_bytes,
            media_type="text/calendar; charset=utf-8",
            headers={"Content-Disposition": f'inline; filename="{filename}"'},
        )


@router.post("/ics/rotate-token")
async def rotate_ics_token(
    faculty_id: UUID | None = Query(None),
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> dict[str, str]:
    """Rotate the personal ICS calendar subscription token."""
    async with uow:
        target_fid = faculty_id
        if target_fid is None:
            profile = await uow.faculty_profiles.get_by_user_id(principal.user_id)
            if profile is None:
                msg = f"FacultyProfile with user_id '{principal.user_id}' was not found"
                raise NotFoundError(msg)
            target_fid = profile.id
        else:
            if principal.role == Role.FACULTY:
                profile = await uow.faculty_profiles.get_by_user_id(principal.user_id)
                if profile is None or profile.id != target_fid:
                    raise ForbiddenError("Faculty can only rotate their own feed token")
            elif principal.role == Role.HOD:
                profile = await uow.faculty_profiles.get_by_id(target_fid)
                if profile is None or profile.department_id != principal.department_id:
                    raise ForbiddenError("HOD can only rotate departmental faculty tokens")

        use_case = RotateIcsTokenUseCase(uow)
        new_token = await use_case.execute(target_fid)
        await uow.commit()
        return {
            "token": new_token,
            "feed_url": f"/api/calendar/ics/{new_token}.ics",
        }
