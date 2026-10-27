from datetime import date
from pathlib import Path
from uuid import uuid4

import pytest

from app.application.security.policy import Principal
from app.application.timetable.confirm import ConfirmTimetableUseCase
from app.application.timetable.parse import ParseTimetableUseCase
from app.application.timetable.upload import UploadTimetableUseCase
from app.core.clock import SystemClock
from app.core.db import async_session_factory
from app.domain import (
    AcademicTerm,
    Department,
    FacultyProfile,
    Initials,
    Role,
    TimetableUploadStatus,
    User,
)
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork
from app.infrastructure.storage.minio_storage import get_storage_service

SAMPLES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "samples" / "timetables"


@pytest.mark.asyncio
async def test_timetable_upload_parse_and_confirm_pipeline() -> None:
    clock = SystemClock()
    storage = get_storage_service()
    dept_id = uuid4()
    term_id = uuid4()
    hod_user_id = uuid4()
    admin_user_id = uuid4()

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        admin = User(
            id=admin_user_id,
            email=f"admin_{uuid4().hex[:6]}@college.edu",
            password_hash="hash",
            role=Role.ADMIN,
        )
        await uow.users.save(admin)

        hod_user = User(
            id=hod_user_id,
            email=f"hod_{uuid4().hex[:6]}@college.edu",
            password_hash="hash",
            role=Role.HOD,
        )
        await uow.users.save(hod_user)

        dept = Department(id=dept_id, code=f"CS_{uuid4().hex[:4]}", name="Computer Science")
        await uow.departments.save(dept)

        term = AcademicTerm(
            id=term_id,
            name="Fall 2026",
            start_date=date(2026, 8, 1),
            end_date=date(2026, 12, 15),
            timezone="Asia/Kolkata",
        )
        await uow.academic_terms.save(term)

        faculty_specs = [
            ("Krish Kumar Sharma", "KKS", "kks@college.edu"),
            ("Rohit Sharma", "RS", "rs@college.edu"),
            ("Amit Patel", "AP", "ap@college.edu"),
        ]
        created_profiles: dict[str, FacultyProfile] = {}
        for name, initials_str, email in faculty_specs:
            u = User(
                id=uuid4(),
                email=f"{uuid4().hex[:6]}_{email}",
                password_hash="hash",
                role=Role.FACULTY,
            )
            await uow.users.save(u)
            prof = FacultyProfile(
                id=uuid4(),
                user_id=u.id,
                department_id=dept_id,
                full_name=name,
                initials=Initials(initials_str),
                email=u.email,
            )
            prof = await uow.faculty_profiles.save(prof)
            created_profiles[initials_str] = prof

        await uow.commit()

    hod_principal = Principal(
        user_id=hod_user_id,
        role=Role.HOD,
        department_id=dept_id,
    )

    xlsx_path = SAMPLES_DIR / "standard_timetable.xlsx"
    xlsx_bytes = xlsx_path.read_bytes()

    upload_uc = UploadTimetableUseCase(
        SqlAlchemyUnitOfWork(async_session_factory), storage, clock
    )
    upload_id = await upload_uc.execute(
        principal=hod_principal,
        department_id=dept_id,
        academic_term_id=term_id,
        file_bytes=xlsx_bytes,
        file_name=xlsx_path.name,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    assert upload_id is not None

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        upload = await uow.timetable_uploads.get_by_id(upload_id)
        assert upload is not None
        assert upload.status == TimetableUploadStatus.UPLOADED

    parse_uc = ParseTimetableUseCase(
        SqlAlchemyUnitOfWork(async_session_factory), storage
    )
    report = await parse_uc.execute(upload_id)

    assert report["total_slots"] == 9
    assert report["unresolved_count"] == 0
    assert len(report["preview_slots"]) == 9

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        upload = await uow.timetable_uploads.get_by_id(upload_id)
        assert upload is not None
        assert upload.status == TimetableUploadStatus.PREVIEW_READY

    confirm_uc = ConfirmTimetableUseCase(
        SqlAlchemyUnitOfWork(async_session_factory), clock
    )
    slots_created, event = await confirm_uc.execute(hod_principal, upload_id)

    assert slots_created == 9
    assert event.slot_count == 9
    assert event.department_id == dept_id

    async with SqlAlchemyUnitOfWork(async_session_factory) as uow:
        upload = await uow.timetable_uploads.get_by_id(upload_id)
        assert upload is not None
        assert upload.status == TimetableUploadStatus.CONFIRMED

        kks_profile = created_profiles["KKS"]
        kks_slots = await uow.timetable_slots.list_by_faculty_id(kks_profile.id)
        assert len(kks_slots) == 5
