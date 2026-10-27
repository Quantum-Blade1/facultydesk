from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

import pytest

from app.core.db import async_session_factory
from app.domain import (
    AcademicTerm,
    AttendeeResponse,
    AuditLog,
    Circular,
    CircularStatus,
    Department,
    Event,
    EventKind,
    EventSource,
    FacultyProfile,
    Holiday,
    Initials,
    NotificationChannel,
    NotificationStatus,
    Role,
    ScheduledNotification,
    Task,
    TaskStatus,
    User,
)
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_round_trip_all_aggregates() -> None:
    uow = SqlAlchemyUnitOfWork(async_session_factory)
    async with uow:
        dept = Department(
            id=uuid4(),
            code=f"CSE_{uuid4().hex[:6]}",
            name="Computer Science and Engineering",
        )
        saved_dept = await uow.departments.save(dept)
        assert saved_dept.code == dept.code
        fetched_dept = await uow.departments.get_by_id(dept.id)
        assert fetched_dept is not None
        assert fetched_dept.name == dept.name

        user = User(
            id=uuid4(),
            email=f"prof_{uuid4().hex[:6]}@college.edu",
            password_hash="argon2id$hashed",
            role=Role.FACULTY,
        )
        saved_user = await uow.users.save(user)
        assert saved_user.email == user.email
        fetched_user = await uow.users.get_by_email(user.email)
        assert fetched_user is not None
        assert fetched_user.id == user.id

        profile = FacultyProfile(
            id=uuid4(),
            user_id=user.id,
            department_id=dept.id,
            full_name="Dr. Krish Kumar",
            initials=Initials("KKS"),
            aliases=("Krish K.", "Prof KKS"),
            email=user.email,
            phone="+919876543210",
        )
        saved_profile = await uow.faculty_profiles.save(profile)
        assert saved_profile.initials.value == "KKS"
        fetched_profile = await uow.faculty_profiles.get_by_department_and_initials(
            dept.id, Initials("KKS")
        )
        assert fetched_profile is not None
        assert fetched_profile.id == profile.id

        term = AcademicTerm(
            id=uuid4(),
            name="Odd Semester 2028",
            start_date=date(2028, 8, 1),
            end_date=date(2028, 12, 15),
            timezone="Asia/Kolkata",
        )
        await uow.academic_terms.save(term)
        active_term = await uow.academic_terms.get_active_term(date(2028, 9, 15))
        assert active_term is not None
        assert active_term.id == term.id

        holiday = Holiday(
            id=uuid4(),
            academic_term_id=term.id,
            date=date(2028, 10, 2),
            label="Gandhi Jayanti",
        )
        await uow.academic_terms.save_holiday(holiday)
        holidays = await uow.academic_terms.list_holidays(term.id)
        assert any(h.id == holiday.id for h in holidays)

        now = datetime.now(UTC)
        event = Event(
            id=uuid4(),
            kind=EventKind.CLASS,
            title="Design and Analysis of Algorithms",
            start_utc=now + timedelta(hours=1),
            end_utc=now + timedelta(hours=2),
            location="Hall A",
            source=EventSource.TIMETABLE,
        )
        event.add_attendee(profile.id, AttendeeResponse.ACCEPTED)
        await uow.events.save(event)

        events_in_range = await uow.events.list_by_faculty_and_range(
            profile.id,
            now,
            now + timedelta(hours=4),
        )
        assert len(events_in_range) == 1
        assert events_in_range[0].id == event.id
        assert events_in_range[0].attendees[0].faculty_id == profile.id

        circ = Circular(
            id=uuid4(),
            file_key="circulars/2026/notice_01.pdf",
            ocr_text="Department meeting on Wednesday at 10 AM",
            confidence=0.92,
            status=CircularStatus.UPLOADED,
        )
        circ.start_processing()
        circ.mark_needs_review({"agenda": "Term Plan"}, 0.92)
        await uow.circulars.save(circ)

        pending_circs = await uow.circulars.list_pending_review()
        assert any(c.id == circ.id for c in pending_circs)

        notif = ScheduledNotification(
            id=uuid4(),
            target_id=event.id,
            target_kind="EVENT",
            user_id=user.id,
            channel=NotificationChannel.EMAIL,
            fire_at_utc=now - timedelta(minutes=5),
            idempotency_key=f"notif_{uuid4().hex}",
            status=NotificationStatus.PENDING,
        )
        await uow.notifications.save(notif)
        due_notifs = await uow.notifications.list_due(now)
        assert any(n.id == notif.id for n in due_notifs)

        task = Task(
            id=uuid4(),
            title="Prepare Lab Rubrics",
            description="Update marks rubrics for OS lab",
            deadline_utc=now + timedelta(days=3),
            importance=4,
            status=TaskStatus.TODO,
            assignee_id=user.id,
            assigner_id=user.id,
        )
        await uow.tasks.save(task)
        user_tasks = await uow.tasks.list_by_assignee(user.id)
        assert any(t.id == task.id for t in user_tasks)

        audit = AuditLog(
            id=uuid4(),
            user_id=user.id,
            action="CREATE_TASK",
            resource_type="Task",
            resource_id=str(task.id),
            payload={"importance": 4},
        )
        await uow.audit_logs.save(audit)
        logs = await uow.audit_logs.list_by_resource("Task", str(task.id))
        assert len(logs) == 1
        assert logs[0].action == "CREATE_TASK"

        await uow.rollback()
