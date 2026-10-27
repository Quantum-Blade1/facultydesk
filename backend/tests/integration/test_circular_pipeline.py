from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest

from app.application.calendar.use_cases import GetCalendarEventsUseCase
from app.application.circulars.use_cases import (
    ConfirmCircularUseCase,
    ProcessCircularUseCase,
)
from app.core.clock import FrozenClock
from app.core.db import async_session_factory
from app.domain.entities import (
    Circular,
    Department,
    FacultyProfile,
    User,
)
from app.domain.value_objects import CircularStatus, Initials, Role
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork


class InMemoryStorageService:
    def __init__(self) -> None:
        self._files: dict[str, bytes] = {}

    def upload_file(
        self,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        self._files[key] = data
        return key

    def download_file(self, key: str) -> bytes:
        if key not in self._files:
            raise KeyError(f"Key not found: {key}")
        return self._files[key]


@pytest.fixture
def sample_dir() -> Path:
    return Path(__file__).parent.parent.parent.parent / "samples" / "circulars"


@pytest.mark.asyncio
async def test_circular_full_pipeline_with_samples(sample_dir: Path) -> None:
    now_utc = datetime(2026, 10, 27, 4, 30, tzinfo=UTC)
    clock = FrozenClock(now_utc)
    storage = InMemoryStorageService()
    process_uc = ProcessCircularUseCase(storage=storage)  # type: ignore[arg-type]

    dept_id = uuid4()
    u1, u2, u3, u4, u5 = uuid4(), uuid4(), uuid4(), uuid4(), uuid4()
    p1, p2, p3, p4, p5 = uuid4(), uuid4(), uuid4(), uuid4(), uuid4()

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        dept = Department(
            id=dept_id,
            name="Computer Science & Engineering",
            code=f"CSE_{uuid4().hex[:4]}",
        )
        await uow.departments.save(dept)

        suffix = uuid4().hex[:6]
        faculty_defs = [
            (u1, p1, "Prof. Krish Sharma", "KKS", f"kks_{suffix}@college.edu"),
            (u2, p2, "Dr. Rajesh Sharma", "RS", f"rs_{suffix}@college.edu"),
            (u3, p3, "Prof. Priya Nair", "PN", f"pn_{suffix}@college.edu"),
            (u4, p4, "Dr. Amit Patel", "AP", f"ap_{suffix}@college.edu"),
            (u5, p5, "Dr. Manoj Kumar Singh", "MKS", f"mks_{suffix}@college.edu"),
        ]

        for uid, pid, name, inits, email in faculty_defs:
            user = User(
                id=uid,
                email=email,
                password_hash="hash",
                role=Role.FACULTY,
            )
            await uow.users.save(user)
            prof = FacultyProfile(
                id=pid,
                user_id=uid,
                department_id=dept_id,
                full_name=name,
                initials=Initials(inits),
            )
            await uow.faculty_profiles.save(prof)

        await uow.commit()

    c1_path = sample_dir / "01_clean_text.pdf"
    assert c1_path.exists()
    c1_bytes = c1_path.read_bytes()
    key1 = "circulars/01_clean_text.pdf"
    storage.upload_file(key1, c1_bytes, "application/pdf")

    c1_id = uuid4()
    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        circular1 = Circular(
            id=c1_id,
            file_key=key1,
            status=CircularStatus.UPLOADED,
            extracted_fields={"department_id": str(dept_id), "filename": "01_clean_text.pdf"},
        )
        await uow.circulars.save(circular1)
        await uow.commit()

        processed1 = await process_uc.execute(c1_id, uow, clock, auto_confirm=False)
        assert processed1.status == CircularStatus.NEEDS_REVIEW
        assert processed1.confidence == 100.0
        fields1 = processed1.extracted_fields
        assert fields1.get("date") == "2026-11-05"
        assert fields1.get("start_time") == "10:30"
        assert fields1.get("is_duration_assumed") is True
        assert "Seminar Hall" in str(fields1.get("venue"))
        attendee_initials = {a["initials"] for a in fields1.get("attendees", [])}
        assert "KKS" in attendee_initials
        assert "RS" in attendee_initials

    c2_path = sample_dir / "02_scanned.pdf"
    assert c2_path.exists()
    c2_bytes = c2_path.read_bytes()
    key2 = "circulars/02_scanned.pdf"
    storage.upload_file(key2, c2_bytes, "application/pdf")

    c2_id = uuid4()
    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        circular2 = Circular(
            id=c2_id,
            file_key=key2,
            status=CircularStatus.UPLOADED,
            extracted_fields={"department_id": str(dept_id), "filename": "02_scanned.pdf"},
        )
        await uow.circulars.save(circular2)
        await uow.commit()

        processed2 = await process_uc.execute(c2_id, uow, clock, auto_confirm=False)
        assert processed2.status == CircularStatus.NEEDS_REVIEW
        fields2 = processed2.extracted_fields
        assert fields2.get("date") == "2026-11-06"
        assert fields2.get("start_time") == "14:00"
        assert fields2.get("end_time") == "16:00"
        assert fields2.get("is_duration_assumed") is False

    c3_path = sample_dir / "03_skewed_phone.jpg"
    assert c3_path.exists()
    c3_bytes = c3_path.read_bytes()
    key3 = "circulars/03_skewed_phone.jpg"
    storage.upload_file(key3, c3_bytes, "image/jpeg")

    c3_id = uuid4()
    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        circular3 = Circular(
            id=c3_id,
            file_key=key3,
            status=CircularStatus.UPLOADED,
            extracted_fields={"department_id": str(dept_id), "filename": "03_skewed_phone.jpg"},
        )
        await uow.circulars.save(circular3)
        await uow.commit()

        processed3 = await process_uc.execute(c3_id, uow, clock, auto_confirm=False)
        assert processed3.status == CircularStatus.NEEDS_REVIEW
        fields3 = processed3.extracted_fields
        assert fields3.get("date") == "2026-11-08"
        assert fields3.get("start_time") == "10:30"
        attendees3 = {a["initials"] for a in fields3.get("attendees", [])}
        assert "KKS" in attendees3 or "MKS" in attendees3

    c4_path = sample_dir / "04_low_light.jpg"
    assert c4_path.exists()
    c4_bytes = c4_path.read_bytes()
    key4 = "circulars/04_low_light.jpg"
    storage.upload_file(key4, c4_bytes, "image/jpeg")

    c4_id = uuid4()
    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        circular4 = Circular(
            id=c4_id,
            file_key=key4,
            status=CircularStatus.UPLOADED,
            extracted_fields={"department_id": str(dept_id), "filename": "04_low_light.jpg"},
        )
        await uow.circulars.save(circular4)
        await uow.commit()

        processed4 = await process_uc.execute(c4_id, uow, clock, auto_confirm=False)
        assert processed4.status == CircularStatus.NEEDS_REVIEW
        fields4 = processed4.extracted_fields
        assert fields4.get("date") == "2026-11-10"
        assert fields4.get("start_time") == "10:30"
        att4 = {a["initials"] for a in fields4.get("attendees", [])}
        assert "KKS" in att4 or "PN" in att4

    c5_path = sample_dir / "05_table_initials.png"
    assert c5_path.exists()
    c5_bytes = c5_path.read_bytes()
    key5 = "circulars/05_table_initials.png"
    storage.upload_file(key5, c5_bytes, "image/png")

    c5_id = uuid4()
    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        circular5 = Circular(
            id=c5_id,
            file_key=key5,
            status=CircularStatus.UPLOADED,
            extracted_fields={"department_id": str(dept_id), "filename": "05_table_initials.png"},
        )
        await uow.circulars.save(circular5)
        await uow.commit()

        processed5 = await process_uc.execute(c5_id, uow, clock, auto_confirm=False)
        assert processed5.status == CircularStatus.NEEDS_REVIEW
        fields5 = processed5.extracted_fields
        assert fields5.get("date") == "2026-11-12"
        assert fields5.get("start_time") == "14:00"
        assert fields5.get("end_time") == "15:30"
        att5 = {a["initials"] for a in fields5.get("attendees", [])}
        assert "KKS" in att5
        assert "RS" in att5
        assert "PN" in att5

    c6_path = sample_dir / "06_all_faculty.pdf"
    assert c6_path.exists()
    c6_bytes = c6_path.read_bytes()
    key6 = "circulars/06_all_faculty.pdf"
    storage.upload_file(key6, c6_bytes, "application/pdf")

    c6_id = uuid4()
    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        circular6 = Circular(
            id=c6_id,
            file_key=key6,
            status=CircularStatus.UPLOADED,
            extracted_fields={"department_id": str(dept_id), "filename": "06_all_faculty.pdf"},
        )
        await uow.circulars.save(circular6)
        await uow.commit()

        processed6 = await process_uc.execute(c6_id, uow, clock, auto_confirm=False)
        assert processed6.status == CircularStatus.NEEDS_REVIEW
        fields6 = processed6.extracted_fields
        assert fields6.get("is_all_faculty") is True
        assert len(fields6.get("attendees", [])) == 5

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        confirm_uc = ConfirmCircularUseCase(uow, clock)
        created_event = await confirm_uc.execute(
            circular_id=c1_id,
        )
        await uow.commit()

        assert created_event is not None
        assert created_event.title == "Meeting on Curriculum and Syllabus Revision for Term 2"

        updated_c1 = await uow.circulars.get_by_id(c1_id)
        assert updated_c1 is not None
        assert updated_c1.status == CircularStatus.CONFIRMED

        cal_uc = GetCalendarEventsUseCase(uow)
        tz = ZoneInfo("Asia/Kolkata")
        q_start = datetime(2026, 11, 5, 0, 0, tzinfo=tz).astimezone(UTC)
        q_end = datetime(2026, 11, 6, 0, 0, tzinfo=tz).astimezone(UTC)
        kks_events = await cal_uc.execute(p1, q_start, q_end)
        assert len(kks_events) == 1
        assert kks_events[0].id == created_event.id

        notifications = await uow.notifications.list_by_target(created_event.id)
        assert len(notifications) >= 1
