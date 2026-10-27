import asyncio
import random
import time
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.domain import EventKind, NotificationChannel, NotificationStatus, Role, TaskStatus
from app.infrastructure.db.models import (
    DepartmentModel,
    EventAttendeeModel,
    EventModel,
    FacultyProfileModel,
    ScheduledNotificationModel,
    TaskModel,
    UserModel,
)

settings = get_settings()


async def run_benchmark() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        dept_res = await session.execute(select(DepartmentModel).limit(1))
        dept = dept_res.scalar_one_or_none()
        if not dept:
            dept = DepartmentModel(
                id=uuid.uuid4(), code="CSE", name="Computer Science and Engineering"
            )
            session.add(dept)
            await session.commit()
        dept_id = dept.id

        faculty_res = await session.execute(select(FacultyProfileModel))
        existing_faculty = list(faculty_res.scalars().all())
        faculty_needed = max(0, 120 - len(existing_faculty))

        if faculty_needed > 0:
            print(f"[*] Seeding {faculty_needed} additional faculty profiles to reach 120...")
            for i in range(faculty_needed):
                idx = len(existing_faculty) + i + 1
                user = UserModel(
                    id=uuid.uuid4(),
                    email=f"bench_faculty_{idx:03d}@facultydesk.local",
                    password_hash="$argon2id$v=19$m=65536,t=3,p=4$dummyhashforbenchmarkonly$dummy",
                    role=Role.FACULTY.value,
                    is_active=True,
                )
                session.add(user)
                profile = FacultyProfileModel(
                    user_id=user.id,
                    department_id=dept_id,
                    employee_id=f"EMP{idx:04d}",
                    full_name=f"Benchmark Faculty {idx:03d}",
                    initials=f"BF{idx:02d}",
                    designation="Assistant Professor",
                    cabin="Lab 3",
                )
                session.add(profile)
                existing_faculty.append(profile)
            await session.commit()

        task_count_res = await session.execute(select(text("COUNT(*) FROM tasks")))
        task_count = task_count_res.scalar() or 0
        tasks_needed = max(0, 5000 - task_count)

        if tasks_needed > 0:
            print(f"[*] Seeding {tasks_needed} additional documentation tasks to reach 5,000...")
            now_utc = datetime.now(UTC)
            for chunk in range(0, tasks_needed, 500):
                batch_size = min(500, tasks_needed - chunk)
                for i in range(batch_size):
                    faculty = random.choice(existing_faculty)
                    task = TaskModel(
                        id=uuid.uuid4(),
                        title=f"Benchmark Task {chunk + i + 1}: Documentation & Compliance",
                        assignee_id=faculty.user_id,
                        assigner_id=existing_faculty[0].user_id,
                        importance=random.randint(1, 5),
                        status=random.choice(
                            [
                                TaskStatus.TODO.value,
                                TaskStatus.IN_PROGRESS.value,
                                TaskStatus.DONE.value,
                            ]
                        ),
                        deadline_utc=now_utc + timedelta(days=random.randint(-10, 45)),
                        created_at_utc=now_utc,
                    )
                    session.add(task)
                await session.commit()

        event_count_res = await session.execute(select(text("COUNT(*) FROM events")))
        event_count = event_count_res.scalar() or 0
        if event_count < 2000:
            print("[*] Seeding timetable events across 2 terms...")
            now_utc = datetime.now(UTC)
            start_term = now_utc - timedelta(days=60)
            for fac in existing_faculty[:60]:
                for day_offset in range(0, 120, 7):
                    for hour in (9, 11, 14):
                        ev_start = start_term + timedelta(days=day_offset, hours=hour)
                        ev_end = ev_start + timedelta(hours=1)
                        event = EventModel(
                            id=uuid.uuid4(),
                            kind=EventKind.CLASS.value,
                            title="Database Management Systems (Lecture)",
                            start_utc=ev_start,
                            end_utc=ev_end,
                            location="Room 402",
                            source="TIMETABLE",
                        )
                        session.add(event)
                        attendee = EventAttendeeModel(
                            id=uuid.uuid4(),
                            event_id=event.id,
                            faculty_id=fac.id,
                        )
                        session.add(attendee)
            await session.commit()

        notif_count_res = await session.execute(
            select(text("COUNT(*) FROM scheduled_notifications WHERE status = 'PENDING'"))
        )
        notif_pending = notif_count_res.scalar() or 0
        if notif_pending < 1000:
            print("[*] Seeding 1,000 pending notifications for claim benchmark...")
            now_utc = datetime.now(UTC)
            for _i in range(1000 - notif_pending):
                fac = random.choice(existing_faculty)
                notif = ScheduledNotificationModel(
                    id=uuid.uuid4(),
                    target_id=uuid.uuid4(),
                    target_kind="EVENT",
                    user_id=fac.user_id,
                    channel=NotificationChannel.PUSH.value,
                    fire_at_utc=now_utc - timedelta(seconds=random.randint(5, 300)),
                    idempotency_key=f"bench_notif_{uuid.uuid4()}",
                    status=NotificationStatus.PENDING.value,
                    attempts=0,
                )
                session.add(notif)
            await session.commit()

        print("[*] Running EXPLAIN (ANALYZE, BUFFERS) on 1-week calendar query...")
        test_faculty = existing_faculty[0].id
        start_w = datetime.now(UTC)
        end_w = start_w + timedelta(days=7)
        cal_explain = await session.execute(
            text(
                """
                EXPLAIN (ANALYZE, BUFFERS)
                SELECT events.id, events.title, events.start_utc, events.end_utc, events.location
                FROM events
                JOIN event_attendees ON event_attendees.event_id = events.id
                WHERE event_attendees.faculty_id = :fac_id
                  AND events.start_utc < :end_utc
                  AND events.end_utc > :start_utc
                ORDER BY events.start_utc;
                """
            ),
            {"fac_id": test_faculty, "start_utc": start_w, "end_utc": end_w},
        )
        print("\n--- 1-Week Calendar Query EXPLAIN ANALYZE ---")
        for row in cal_explain:
            print(row[0])

        print("\n[*] Measuring 1-week calendar query latency across 50 requests...")
        latencies: list[float] = []
        for _ in range(50):
            fac_id = random.choice(existing_faculty).id
            t0 = time.perf_counter()
            await session.execute(
                text(
                    """
                    SELECT events.id, events.title, events.start_utc,
                           events.end_utc, events.location
                    FROM events
                    JOIN event_attendees ON event_attendees.event_id = events.id
                    WHERE event_attendees.faculty_id = :fac_id
                      AND events.start_utc < :end_utc
                      AND events.end_utc > :start_utc
                    ORDER BY events.start_utc;
                    """
                ),
                {"fac_id": fac_id, "start_utc": start_w, "end_utc": end_w},
            )
            latencies.append((time.perf_counter() - t0) * 1000.0)

        latencies.sort()
        p50 = latencies[int(len(latencies) * 0.50)]
        p95 = latencies[int(len(latencies) * 0.95)]
        p99 = latencies[int(len(latencies) * 0.99)]
        summary = (
            f"Calendar query latencies (ms): min={latencies[0]:.2f}ms, "
            f"p50={p50:.2f}ms, p95={p95:.2f}ms, p99={p99:.2f}ms"
        )
        print(summary)
        assert p95 < 150.0, f"Calendar p95 {p95:.2f}ms exceeded target 150ms"
        print("[✓] Calendar query p95 meets target (< 150ms)")

        print("\n[*] Running EXPLAIN (ANALYZE, BUFFERS) on 1,000 due notification claim query...")
        now_utc = datetime.now(UTC)
        notif_explain = await session.execute(
            text(
                """
                EXPLAIN (ANALYZE, BUFFERS)
                SELECT id, target_id, target_kind, user_id, channel, fire_at_utc, status
                FROM scheduled_notifications
                WHERE status = 'PENDING'
                  AND fire_at_utc <= :up_to_utc
                ORDER BY fire_at_utc ASC
                LIMIT 1000
                FOR UPDATE SKIP LOCKED;
                """
            ),
            {"up_to_utc": now_utc},
        )
        print("\n--- 1,000 Due Notification Claim Query EXPLAIN ANALYZE ---")
        for row in notif_explain:
            print(row[0])

        print("\n[*] Measuring 1,000 due notification claim execution duration...")
        t0 = time.perf_counter()
        claim_res = await session.execute(
            text(
                """
                SELECT id, target_id, target_kind, user_id, channel, fire_at_utc, status
                FROM scheduled_notifications
                WHERE status = 'PENDING'
                  AND fire_at_utc <= :up_to_utc
                ORDER BY fire_at_utc ASC
                LIMIT 1000
                FOR UPDATE SKIP LOCKED;
                """
            ),
            {"up_to_utc": now_utc},
        )
        claimed = claim_res.fetchall()
        duration_s = time.perf_counter() - t0
        print(f"Claimed {len(claimed)} notifications in {duration_s:.4f}s")
        assert duration_s < 60.0, f"Notification claim batch exceeded target 60s: {duration_s}s"
        print("[✓] Notification claim batch meets target (< 60s)")

    await engine.dispose()
    print("\n[✓] All Stage 10 performance benchmarks completed successfully!")


if __name__ == "__main__":
    asyncio.run(run_benchmark())
