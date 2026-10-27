import secrets
from datetime import UTC, date, datetime, time, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from app.application.calendar.free_slots import BusyInterval, FreeSlotFinder
from app.application.calendar.ics_service import generate_vcalendar_ics
from app.application.calendar.recurrence import expand_slot_recurrence
from app.application.reminders.planner import ReminderPlanner
from app.core.clock import Clock
from app.domain.entities import Event, EventAttendee
from app.domain.errors import ClashDetectedError, EntityNotFound
from app.domain.events import EventScheduled
from app.domain.repositories import UnitOfWork
from app.domain.value_objects import AttendeeResponse, EventKind, EventSource


class MaterialiseTimetableEventsUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(self, upload_id: UUID | None = None) -> int:
        tz = ZoneInfo("Asia/Kolkata")
        today = self._clock.now().astimezone(tz).date()
        window_start = today
        window_end = today + timedelta(days=21)

        slots = []
        if upload_id is not None:
            upload = await self._uow.timetable_uploads.get_by_id(upload_id)
            if upload is None:
                raise EntityNotFound("TimetableUpload", str(upload_id))
            slots = await self._uow.timetable_slots.list_by_upload_id(upload_id)
            term = await self._uow.academic_terms.get_by_id(upload.academic_term_id)
        else:
            term = await self._uow.academic_terms.get_active_term(today)
            if term is None:
                return 0
            term_uploads = await self._uow.timetable_uploads.list_by_term_id(term.id)
            for up in term_uploads:
                if up.status.value == "CONFIRMED":
                    up_slots = await self._uow.timetable_slots.list_by_upload_id(up.id)
                    slots.extend(up_slots)



        if term is None:
            return 0

        holidays_list = await self._uow.academic_terms.list_holidays(term.id)
        holidays = {h.date for h in holidays_list}

        count = 0
        for slot in slots:
            occurrences = expand_slot_recurrence(
                slot=slot,
                term=term,
                holidays=holidays,
                window_start=window_start,
                window_end=window_end,
            )
            course = await self._uow.courses.get_by_id(slot.course_id)
            section = await self._uow.sections.get_by_id(slot.section_id)
            room = await self._uow.rooms.get_by_id(slot.room_id)

            title = f"{course.code} ({section.name})" if course and section else "Class"
            location = room.code if room else ""

            for occ_date, start_utc, end_utc in occurrences:
                existing = await self._uow.events.get_by_slot_and_date(slot.id, occ_date)
                if existing is not None:
                    continue

                event = Event(
                    kind=EventKind.CLASS,
                    title=title,
                    start_utc=start_utc,
                    end_utc=end_utc,
                    location=location,
                    source=EventSource.TIMETABLE,
                    source_id=slot.id,
                    recurrence_date=occ_date,
                )
                event.add_attendee(slot.faculty_id, AttendeeResponse.ACCEPTED)
                saved = await self._uow.events.save(event)
                saved.domain_events.append(
                    EventScheduled(
                        scheduled_event_id=saved.id,
                        title=saved.title,
                        start_utc=saved.start_utc,
                        end_utc=saved.end_utc,
                        attendee_ids=(slot.faculty_id,),
                    )
                )
                planner = ReminderPlanner(self._clock)
                await planner.plan_event_reminders(saved, self._uow)
                count += 1

        return count


class GetCalendarEventsUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
        self, faculty_id: UUID, start_utc: datetime, end_utc: datetime
    ) -> list[Event]:
        return await self._uow.events.list_by_faculty_and_range(
            faculty_id, start_utc, end_utc
        )


class CheckClashesUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
        self,
        start_utc: datetime,
        end_utc: datetime,
        attendee_ids: list[UUID],
        exclude_event_id: UUID | None = None,
    ) -> list[dict[str, str]]:
        clashes: list[dict[str, str]] = []
        for aid in attendee_ids:
            events = await self._uow.events.list_by_faculty_and_range(
                aid, start_utc, end_utc
            )
            profile = await self._uow.faculty_profiles.get_by_id(aid)
            faculty_name = profile.full_name if profile else ""
            for ev in events:
                if exclude_event_id is not None and ev.id == exclude_event_id:
                    continue
                if start_utc < ev.end_utc and ev.start_utc < end_utc:
                    clashes.append(
                        {
                            "faculty_id": str(aid),
                            "faculty_name": faculty_name,
                            "event_id": str(ev.id),
                            "event_title": ev.title,
                            "start_utc": ev.start_utc.isoformat(),
                            "end_utc": ev.end_utc.isoformat(),
                        }
                    )
        return clashes


class CreateEventUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        kind: EventKind,
        title: str,
        start_utc: datetime,
        end_utc: datetime,
        location: str,
        attendee_ids: list[UUID],
        override_clashes: bool = False,
        source: EventSource = EventSource.MANUAL,
    ) -> Event:
        checker = CheckClashesUseCase(self._uow)
        clashes = await checker.execute(start_utc, end_utc, attendee_ids)
        if clashes and not override_clashes:
            raise ClashDetectedError(
                f"Clashes detected for {len(clashes)} attendee event(s)",
                clashes=clashes,
            )

        event = Event(
            kind=kind,
            title=title,
            start_utc=start_utc,
            end_utc=end_utc,
            location=location,
            source=source,
        )
        for aid in attendee_ids:
            event.add_attendee(aid, AttendeeResponse.INVITED)

        saved = await self._uow.events.save(event)
        saved.domain_events.append(
            EventScheduled(
                scheduled_event_id=saved.id,
                title=saved.title,
                start_utc=saved.start_utc,
                end_utc=saved.end_utc,
                attendee_ids=tuple(attendee_ids),
            )
        )
        planner = ReminderPlanner(self._clock)
        await planner.plan_event_reminders(saved, self._uow)
        return saved


class UpdateEventUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock | None = None) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        event_id: UUID,
        title: str | None = None,
        location: str | None = None,
        start_utc: datetime | None = None,
        end_utc: datetime | None = None,
        attendee_ids: list[UUID] | None = None,
        override_clashes: bool = False,
    ) -> Event:
        event = await self._uow.events.get_by_id(event_id)
        if event is None:
            raise EntityNotFound("Event", str(event_id))

        rescheduled = False
        if start_utc is not None and end_utc is not None:
            target_aids = (
                attendee_ids
                if attendee_ids is not None
                else [att.faculty_id for att in event.attendees]
            )
            checker = CheckClashesUseCase(self._uow)
            clashes = await checker.execute(
                start_utc, end_utc, target_aids, exclude_event_id=event_id
            )
            if clashes and not override_clashes:
                raise ClashDetectedError(
                    f"Clashes detected for {len(clashes)} attendee event(s)",
                    clashes=clashes,
                )
            event.reschedule(start_utc, end_utc)
            rescheduled = True

        if title is not None:
            event.title = title
        if location is not None:
            event.location = location
        if attendee_ids is not None:
            existing = {att.faculty_id: att for att in event.attendees}
            new_attendees = []
            for aid in attendee_ids:
                if aid in existing:
                    new_attendees.append(existing[aid])
                else:
                    new_attendees.append(
                        EventAttendee(
                            event_id=event.id,
                            faculty_id=aid,
                            response=AttendeeResponse.INVITED,
                        )
                    )
            event.attendees = new_attendees

        saved = await self._uow.events.save(event)
        if rescheduled and self._clock is not None:
            planner = ReminderPlanner(self._clock)
            await planner.handle_event_rescheduled(saved, self._uow)

        return saved


class CancelEventUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock | None = None) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(self, event_id: UUID, reason: str = "") -> None:
        event = await self._uow.events.get_by_id(event_id)
        if event is None:
            raise EntityNotFound("Event", str(event_id))

        event.cancel(reason)
        if self._clock is not None:
            planner = ReminderPlanner(self._clock)
            await planner.handle_event_cancelled(event_id, self._uow)
        await self._uow.events.delete(event_id)


class FindFreeSlotsUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
        self,
        attendee_ids: list[UUID],
        start_date: date,
        end_date: date,
        duration_minutes: int,
        work_start_time: time = time(8, 0),
        work_end_time: time = time(18, 0),
        timezone_str: str = "Asia/Kolkata",
    ) -> list[tuple[datetime, datetime]]:
        tz = ZoneInfo(timezone_str)
        ws_local = datetime.combine(start_date, time.min, tzinfo=tz)
        we_local = datetime.combine(end_date, time.max, tzinfo=tz)
        query_start_utc = ws_local.astimezone(UTC)
        query_end_utc = we_local.astimezone(UTC)

        busy_intervals: list[BusyInterval] = []
        for aid in attendee_ids:
            events = await self._uow.events.list_by_faculty_and_range(
                aid, query_start_utc, query_end_utc
            )
            for ev in events:
                busy_intervals.append(
                    BusyInterval(start_utc=ev.start_utc, end_utc=ev.end_utc)
                )

        finder = FreeSlotFinder(
            work_start_time=work_start_time,
            work_end_time=work_end_time,
            timezone_str=timezone_str,
        )
        return finder.find_free_slots(
            busy_intervals=busy_intervals,
            start_date=start_date,
            end_date=end_date,
            min_duration_minutes=duration_minutes,
        )


class GenerateIcsFeedUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(self, feed_token: str) -> tuple[str, bytes]:
        profile = await self._uow.faculty_profiles.get_by_ics_token(feed_token)
        if profile is None:
            raise EntityNotFound("FacultyProfile", "ics_token")

        now = self._clock.now()
        start_utc = now - timedelta(days=30)
        end_utc = now + timedelta(days=90)

        events = await self._uow.events.list_by_faculty_and_range(
            profile.id, start_utc, end_utc
        )
        ics_bytes = generate_vcalendar_ics(
            events=events,
            calendar_name=f"{profile.full_name}'s Schedule",
            timestamp_utc=now,
        )
        filename = f"{profile.initials.value}_schedule.ics"
        return filename, ics_bytes


class RotateIcsTokenUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, faculty_id: UUID) -> str:
        profile = await self._uow.faculty_profiles.get_by_id(faculty_id)
        if profile is None:
            raise EntityNotFound("FacultyProfile", str(faculty_id))

        new_token = secrets.token_urlsafe(32)
        profile.ics_token = new_token
        await self._uow.faculty_profiles.save(profile)
        return new_token
