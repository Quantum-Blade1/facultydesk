import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

import httpx
import pytest

from app.application.calendar.use_cases import (
    CancelEventUseCase,
    CreateEventUseCase,
    UpdateEventUseCase,
)
from app.application.reminders.dispatcher import ReminderDispatcher
from app.application.reminders.planner import ReminderPlanner
from app.core.clock import FrozenClock
from app.core.config import get_settings
from app.core.db import async_session_factory
from app.domain.entities import Department, Event, FacultyProfile, ScheduledNotification, User
from app.domain.repositories import UnitOfWork
from app.domain.value_objects import (
    EventKind,
    Initials,
    NotificationChannel,
    NotificationStatus,
    Role,
)
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork
from app.infrastructure.notifiers.base import NotificationPayload, Notifier
from app.infrastructure.notifiers.email import EmailNotifier


class ConcurrentMockNotifier(Notifier):
    def __init__(self) -> None:
        self.sent_notification_ids: list[UUID] = []
        self._lock = asyncio.Lock()

    async def send(
        self,
        notification: ScheduledNotification,
        payload: NotificationPayload,
        recipient_user: User,
        recipient_profile: FacultyProfile | None,
        uow: UnitOfWork,
    ) -> None:
        async with self._lock:
            self.sent_notification_ids.append(notification.id)


@pytest.mark.asyncio
async def test_concurrency_dispatcher_skip_locked() -> None:
    now_utc = datetime(2026, 10, 28, 10, 0, tzinfo=UTC)
    clock = FrozenClock(now_utc)
    mock_notifier = ConcurrentMockNotifier()

    dispatcher1 = ReminderDispatcher(clock, mock_notifier, "http://localhost:3000")
    dispatcher2 = ReminderDispatcher(clock, mock_notifier, "http://localhost:3000")

    user_id = uuid4()
    dept_id = uuid4()
    profile_id = uuid4()
    target_id = uuid4()
    notification_ids: list[UUID] = []

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        dept = Department(id=dept_id, name="CSE", code=f"CS_{uuid4().hex[:4]}")
        await uow.departments.save(dept)

        user = User(
            id=user_id,
            email=f"concurrency_{uuid4().hex[:6]}@college.edu",
            password_hash="hash",
            role=Role.FACULTY,
        )
        await uow.users.save(user)

        profile = FacultyProfile(
            id=profile_id,
            user_id=user_id,
            department_id=dept_id,
            full_name="Concurrency Faculty",
            initials=Initials("CCF"),
        )
        await uow.faculty_profiles.save(profile)

        event = Event(
            id=target_id,
            kind=EventKind.MEETING,
            title="Concurrency Benchmark Event",
            start_utc=now_utc + timedelta(hours=1),
            end_utc=now_utc + timedelta(hours=2),
            location="Auditorium",
        )
        await uow.events.save(event)

        for i in range(500):
            nid = uuid4()
            notification_ids.append(nid)
            n = ScheduledNotification(
                id=nid,
                target_id=target_id,
                target_kind="EVENT",
                user_id=user_id,
                channel=NotificationChannel.EMAIL,
                fire_at_utc=now_utc - timedelta(seconds=i + 1),
                idempotency_key=f"bench_key_{i}_{uuid4().hex}",
                status=NotificationStatus.PENDING,
            )
            await uow.notifications.save(n)
        await uow.commit()

    uow1 = SqlAlchemyUnitOfWork(async_session_factory)
    uow2 = SqlAlchemyUnitOfWork(async_session_factory)

    async def run_d1() -> int:
        total = 0
        while True:
            c = await dispatcher1.dispatch_due(uow1, batch_size=50)
            total += c
            if c == 0:
                break
        return total

    async def run_d2() -> int:
        total = 0
        while True:
            c = await dispatcher2.dispatch_due(uow2, batch_size=50)
            total += c
            if c == 0:
                break
        return total

    await asyncio.gather(run_d1(), run_d2())

    target_ids_set = set(notification_ids)
    target_sent = [
        nid for nid in mock_notifier.sent_notification_ids if nid in target_ids_set
    ]
    assert len(target_sent) == 500
    assert len(set(target_sent)) == 500
    assert len(set(mock_notifier.sent_notification_ids)) == len(mock_notifier.sent_notification_ids)

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        pending = await uow.notifications.claim_due_batch(now_utc, limit=10)
        assert len(pending) == 0


@pytest.mark.asyncio
async def test_planning_idempotency_property() -> None:
    now_utc = datetime(2026, 10, 28, 10, 0, tzinfo=UTC)
    clock = FrozenClock(now_utc)
    user_id = uuid4()
    dept_id = uuid4()
    profile_id = uuid4()
    event_id = uuid4()

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        dept = Department(id=dept_id, name="ECE", code=f"EC_{uuid4().hex[:4]}")
        await uow.departments.save(dept)

        user = User(
            id=user_id,
            email=f"idemp_{uuid4().hex[:6]}@college.edu",
            password_hash="hash",
            role=Role.FACULTY,
        )
        await uow.users.save(user)

        profile = FacultyProfile(
            id=profile_id,
            user_id=user_id,
            department_id=dept_id,
            full_name="Test Planner Faculty",
            initials=Initials("TPF"),
        )
        await uow.faculty_profiles.save(profile)

        event = Event(
            id=event_id,
            kind=EventKind.MEETING,
            title="Faculty Board Meeting",
            start_utc=now_utc + timedelta(hours=2),
            end_utc=now_utc + timedelta(hours=3),
            location="Room 101",
        )
        event.add_attendee(profile_id)
        await uow.events.save(event)

        planner = ReminderPlanner(clock)
        first_run = await planner.plan_event_reminders(event, uow)
        assert len(first_run) > 0

        second_run = await planner.plan_event_reminders(event, uow)
        assert len(second_run) == len(first_run)

        rows = await uow.notifications.list_by_target(event_id)
        assert len(rows) == len(first_run)


@pytest.mark.asyncio
async def test_reschedule_and_cancel_lifecycle() -> None:
    now_utc = datetime(2026, 10, 28, 10, 0, tzinfo=UTC)
    clock = FrozenClock(now_utc)
    user_id = uuid4()
    dept_id = uuid4()
    profile_id = uuid4()

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        dept = Department(id=dept_id, name="Mechanical", code=f"ME_{uuid4().hex[:4]}")
        await uow.departments.save(dept)

        user = User(
            id=user_id,
            email=f"attendee_{uuid4().hex[:6]}@college.edu",
            password_hash="hash",
            role=Role.FACULTY,
        )
        await uow.users.save(user)

        profile = FacultyProfile(
            id=profile_id,
            user_id=user_id,
            department_id=dept_id,
            full_name="Lifecycle Faculty",
            initials=Initials("LCF"),
        )
        await uow.faculty_profiles.save(profile)
        await uow.commit()

    start_1 = now_utc + timedelta(hours=5)
    end_1 = now_utc + timedelta(hours=6)

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        create_uc = CreateEventUseCase(uow, clock)
        event_res = await create_uc.execute(
            kind=EventKind.MEETING,
            title="Department Review",
            start_utc=start_1,
            end_utc=end_1,
            location="Board Room",
            attendee_ids=[profile_id],
        )
        await uow.commit()

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        initial_notifs = await uow.notifications.list_by_target(event_res.id)
        assert len(initial_notifs) > 0
        assert all(n.status == NotificationStatus.PENDING for n in initial_notifs)
        old_fire_times = {n.id: n.fire_at_utc for n in initial_notifs}

    start_2 = now_utc + timedelta(hours=8)
    end_2 = now_utc + timedelta(hours=9)

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        update_uc = UpdateEventUseCase(uow, clock)
        await update_uc.execute(
            event_id=event_res.id,
            title="Department Review Rescheduled",
            start_utc=start_2,
            end_utc=end_2,
            location="Board Room",
            attendee_ids=[profile_id],
        )
        await uow.commit()

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        rescheduled_notifs = await uow.notifications.list_by_target(event_res.id)
        pending = [n for n in rescheduled_notifs if n.status == NotificationStatus.PENDING]
        assert len(pending) == len(initial_notifs)
        for n in pending:
            assert n.fire_at_utc > old_fire_times[n.id]

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        cancel_uc = CancelEventUseCase(uow, clock)
        await cancel_uc.execute(event_id=event_res.id)
        await uow.commit()

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        final_notifs = await uow.notifications.list_by_target(event_res.id)
        assert all(n.status == NotificationStatus.CANCELLED for n in final_notifs)


@pytest.mark.asyncio
async def test_mailpit_real_delivery() -> None:
    settings = get_settings()
    recipient_email = f"live_test_{uuid4().hex[:6]}@college.edu"
    smtp_host = "127.0.0.1" if settings.SMTP_HOST == "mailpit" else settings.SMTP_HOST

    notifier = EmailNotifier(
        hostname=smtp_host,
        port=settings.SMTP_PORT,
        sender=settings.SMTP_FROM,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
    )

    dummy_user = User(
        id=uuid4(),
        email=recipient_email,
        password_hash="hash",
        role=Role.FACULTY,
    )
    dummy_notif = ScheduledNotification(
        id=uuid4(),
        target_id=uuid4(),
        target_kind="EVENT",
        user_id=dummy_user.id,
        channel=NotificationChannel.EMAIL,
        fire_at_utc=datetime.now(UTC),
    )
    payload = NotificationPayload(
        title="Autonomous Verification Meeting",
        body="Autonomous Verification Meeting reminder",
        start_time_local="2026-10-28 10:30 IST",
        venue="Auditorium",
        deep_link="http://localhost:3000/calendar",
        event_id=dummy_notif.target_id,
    )

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        await notifier.send(dummy_notif, payload, dummy_user, None, uow)

    async with httpx.AsyncClient() as client:
        resp = await client.get("http://127.0.0.1:8025/api/v1/messages")
        assert resp.status_code == 200
        data: dict[str, Any] = resp.json()
        messages: list[dict[str, Any]] = data.get("messages", [])
        matched = [
            m
            for m in messages
            if any(recipient_email in to_item.get("Address", "") for to_item in m.get("To", []))
        ]
        assert len(matched) >= 1
        msg_id = matched[0]["ID"]

        detail_resp = await client.get(f"http://127.0.0.1:8025/api/v1/message/{msg_id}")
        assert detail_resp.status_code == 200
        detail_data: dict[str, Any] = detail_resp.json()
        assert "Autonomous Verification Meeting" in detail_data.get("Subject", "")
        assert "Auditorium" in detail_data.get("Text", "")
        assert "FacultyDesk Notification Engine" in detail_data.get("HTML", "")
