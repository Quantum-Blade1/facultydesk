from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest

from app.application.directory.bulk_import import BulkImportFacultyUseCase
from app.application.security.policy import Principal
from app.core.clock import FrozenClock
from app.core.db import async_session_factory
from app.domain import Department, FacultyProfile, Initials, Role, User
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_bulk_import_from_sample_csv() -> None:
    csv_path = Path(__file__).parents[3] / "samples" / "faculty.csv"
    assert csv_path.exists()
    content = csv_path.read_bytes()

    uow = SqlAlchemyUnitOfWork(async_session_factory)
    clock = FrozenClock(datetime(2026, 10, 27, 12, 0, tzinfo=UTC))
    dept_id = uuid4()
    admin_user = User(
        id=uuid4(),
        email=f"admin_{uuid4().hex[:4]}@college.edu",
        password_hash="hash",
        role=Role.ADMIN,
        is_active=True,
    )
    admin = Principal(user_id=admin_user.id, role=Role.ADMIN)

    async with uow:
        await uow.users.save(admin_user)
        dept = Department(
            id=dept_id,
            code=f"BI_{uuid4().hex[:4].upper()}",
            name="Bulk Import Department",
        )
        await uow.departments.save(dept)

        existing_user = User(
            id=uuid4(),
            email=f"kks_{uuid4().hex[:4]}@college.edu",
            password_hash="hash",
            role=Role.FACULTY,
            is_active=True,
        )
        await uow.users.save(existing_user)

        existing_profile = FacultyProfile(
            id=uuid4(),
            user_id=existing_user.id,
            department_id=dept_id,
            full_name="Existing Faculty KKS",
            initials=Initials("KKS"),
            aliases=(),
            email=existing_user.email,
        )
        await uow.faculty_profiles.save(existing_profile)
        await uow.commit()

    use_case = BulkImportFacultyUseCase(uow, clock)
    report = await use_case.execute(
        principal=admin,
        department_id=dept_id,
        file_content=content,
        file_extension="csv",
    )

    assert report.total_rows == 5
    assert report.created_count + report.updated_count == 2
    assert report.rejected_count == 3

    assert all(r.status in ("CREATED", "UPDATED") for r in report.rows[:2])
    assert all(r.status == "REJECTED" for r in report.rows[2:])

    assert "Invalid email format" in report.rows[2].message
    assert "Duplicate initials" in report.rows[3].message
    assert "already taken" in report.rows[4].message
