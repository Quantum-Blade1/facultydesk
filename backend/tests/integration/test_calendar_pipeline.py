from datetime import UTC, date, datetime, time, timedelta
from uuid import uuid4
from zoneinfo import ZoneInfo

import icalendar
import pytest

from app.application.calendar.use_cases import (
    CheckClashesUseCase,
    CreateEventUseCase,
    FindFreeSlotsUseCase,
    GenerateIcsFeedUseCase,
    GetCalendarEventsUseCase,
    RotateIcsTokenUseCase,
)
from app.application.security.policy import Principal
from app.application.timetable.confirm import ConfirmTimetableUseCase
from app.core.clock import FrozenClock
from app.core.db import async_session_factory
from app.domain.entities import (
    AcademicTerm,
    Department,
    FacultyProfile,
    Holiday,
    TimetableUpload,
    User,
)
from app.domain.errors import ClashDetectedError, EntityNotFound
from app.domain.value_objects import (
    EventKind,
    Initials,
    Role,
    TimetableUploadStatus,
)
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_calendar_full_pipeline() -> None:
    now_utc = datetime(2026, 10, 26, 4, 30, tzinfo=UTC)
    clock = FrozenClock(now_utc)

    dept_id = uuid4()
    term_id = uuid4()
    kks_user_id = uuid4()
    kks_profile_id = uuid4()
    rs_user_id = uuid4()
    rs_profile_id = uuid4()
    admin_user_id = uuid4()
    upload_id = uuid4()

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        admin = User(
            id=admin_user_id,
            email=f"admin_{uuid4().hex[:6]}@college.edu",
            password_hash="hash",
            role=Role.ADMIN,
        )
        await uow.users.save(admin)

        kks_user = User(
            id=kks_user_id,
            email=f"kks_{uuid4().hex[:6]}@college.edu",
            password_hash="hash",
            role=Role.FACULTY,
        )
        await uow.users.save(kks_user)

        rs_user = User(
            id=rs_user_id,
            email=f"rs_{uuid4().hex[:6]}@college.edu",
            password_hash="hash",
            role=Role.FACULTY,
        )
        await uow.users.save(rs_user)

        dept = Department(id=dept_id, code=f"CS_{uuid4().hex[:4]}", name="Computer Science")
        await uow.departments.save(dept)

        kks_profile = FacultyProfile(
            id=kks_profile_id,
            user_id=kks_user_id,
            department_id=dept_id,
            full_name="Krish Kumar Sharma",
            initials=Initials("KKS"),
            email=kks_user.email,
        )
        await uow.faculty_profiles.save(kks_profile)

        rs_profile = FacultyProfile(
            id=rs_profile_id,
            user_id=rs_user_id,
            department_id=dept_id,
            full_name="Ravi Sharma",
            initials=Initials("RS"),
            email=rs_user.email,
        )
        await uow.faculty_profiles.save(rs_profile)

        term = AcademicTerm(
            id=term_id,
            name="Autumn 2026",
            start_date=date(2026, 8, 1),
            end_date=date(2026, 12, 15),
            timezone="Asia/Kolkata",
        )
        await uow.academic_terms.save(term)

        diwali = Holiday(
            id=uuid4(),
            academic_term_id=term_id,
            date=date(2026, 10, 28),
            label="Diwali",
        )
        await uow.academic_terms.save_holiday(diwali)

        upload = TimetableUpload(
            id=upload_id,
            department_id=dept_id,
            academic_term_id=term_id,
            file_key="timetables/test.xlsx",
            status=TimetableUploadStatus.PREVIEW_READY,
            parse_report={
                "preview_slots": [
                    {
                        "course_code": "CS301",
                        "course_name": "Computer Networks",
                        "section_name": "A",
                        "room_code": "LH-101",
                        "weekday": 2,
                        "start_time": "10:00:00",
                        "end_time": "11:45:00",
                        "faculty_id": str(kks_profile_id),
                        "source_cell": "B2",
                    }
                ],
                "unresolved_tokens": [],
            },

        )
        await uow.timetable_uploads.save(upload)
        await uow.commit()

    admin_principal = Principal(user_id=admin_user_id, role=Role.ADMIN)

    confirm_uc = ConfirmTimetableUseCase(
        SqlAlchemyUnitOfWork(async_session_factory), clock
    )
    slots_created, _event = await confirm_uc.execute(admin_principal, upload_id)
    assert slots_created == 1


    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        calendar_uc = GetCalendarEventsUseCase(uow)
        events = await calendar_uc.execute(
            faculty_id=kks_profile_id,
            start_utc=datetime(2026, 10, 26, 0, 0, tzinfo=UTC),
            end_utc=datetime(2026, 11, 20, 0, 0, tzinfo=UTC),
        )

        occ_dates = [ev.recurrence_date for ev in events if ev.recurrence_date is not None]
        assert date(2026, 10, 28) not in occ_dates
        assert date(2026, 11, 4) in occ_dates
        assert date(2026, 11, 11) in occ_dates

    clash_start_local = datetime(2026, 11, 4, 10, 30, tzinfo=ZoneInfo("Asia/Kolkata"))
    clash_end_local = datetime(2026, 11, 4, 11, 30, tzinfo=ZoneInfo("Asia/Kolkata"))
    clash_start_utc = clash_start_local.astimezone(UTC)
    clash_end_utc = clash_end_local.astimezone(UTC)

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        checker = CheckClashesUseCase(uow)
        clash_reports = await checker.execute(
            start_utc=clash_start_utc,
            end_utc=clash_end_utc,
            attendee_ids=[kks_profile_id],
        )
        assert len(clash_reports) >= 1
        assert "CS301 (A)" in clash_reports[0]["event_title"]

        create_uc = CreateEventUseCase(uow, clock)
        with pytest.raises(ClashDetectedError) as exc_info:
            await create_uc.execute(
                kind=EventKind.MEETING,
                title="Curriculum Committee",
                start_utc=clash_start_utc,
                end_utc=clash_end_utc,
                location="Conference Room",
                attendee_ids=[kks_profile_id],
                override_clashes=False,
            )
        assert len(exc_info.value.clashes) >= 1

        meeting = await create_uc.execute(
            kind=EventKind.MEETING,
            title="Curriculum Committee",
            start_utc=clash_start_utc,
            end_utc=clash_end_utc,
            location="Conference Room",
            attendee_ids=[kks_profile_id],
            override_clashes=True,
        )
        await uow.commit()
        assert meeting.title == "Curriculum Committee"

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        free_slots_uc = FindFreeSlotsUseCase(uow)
        free_slots = await free_slots_uc.execute(
            attendee_ids=[kks_profile_id, rs_profile_id],
            start_date=date(2026, 11, 4),
            end_date=date(2026, 11, 4),
            duration_minutes=60,
            work_start_time=time(8, 0),
            work_end_time=time(18, 0),
        )
        assert len(free_slots) > 0
        for fs_start, fs_end in free_slots:
            assert (fs_end - fs_start) >= timedelta(minutes=60)

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        profile = await uow.faculty_profiles.get_by_id(kks_profile_id)
        assert profile is not None
        feed_token = profile.ics_token

        ics_uc = GenerateIcsFeedUseCase(uow, clock)
        filename, ics_bytes = await ics_uc.execute(feed_token)
        assert filename == "KKS_schedule.ics"
        assert len(ics_bytes) > 0

        cal = icalendar.Calendar.from_ical(ics_bytes)
        assert cal.get("version") == "2.0"
        vevents = [c for c in cal.subcomponents if c.name == "VEVENT"]
        assert len(vevents) >= 2

        rotate_uc = RotateIcsTokenUseCase(uow)
        new_token = await rotate_uc.execute(kks_profile_id)
        await uow.commit()
        assert new_token != feed_token

        with pytest.raises(EntityNotFound):
            await ics_uc.execute(feed_token)

        new_filename, new_bytes = await ics_uc.execute(new_token)
        assert new_filename == "KKS_schedule.ics"
        assert len(new_bytes) > 0
