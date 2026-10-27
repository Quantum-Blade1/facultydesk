from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from app.application.tasks.use_cases import (
    AssignTaskUseCase,
    CompleteTaskUseCase,
    CreateTaskUseCase,
    GetHodDashboardUseCase,
    ListTasksUseCase,
    ListTaskTemplatesUseCase,
    ReopenTaskUseCase,
)
from app.core.clock import FrozenClock
from app.core.db import async_session_factory
from app.core.security import hash_password
from app.domain import (
    Department,
    FacultyProfile,
    Initials,
    NotificationStatus,
    Role,
    TaskCategory,
    TaskStatus,
    TaskTemplate,
    User,
)
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_task_creation_and_assignment_pipeline() -> None:
    now_utc = datetime(2026, 10, 28, 9, 0, tzinfo=UTC)
    clock = FrozenClock(now_utc)
    uow = SqlAlchemyUnitOfWork(async_session_factory)

    tag = uuid4().hex[:6]
    dept_id = uuid4()
    dept = Department(id=dept_id, code=f"D{tag[:3].upper()}", name="Department of Testing")

    hod_id = uuid4()
    hod_user = User(
        id=hod_id,
        email=f"hod_{tag}@facultydesk.local",
        password_hash=hash_password("Pass123!"),
        role=Role.HOD,
        is_active=True,
    )
    hod_profile = FacultyProfile(
        id=uuid4(),
        user_id=hod_id,
        department_id=dept_id,
        full_name="Dr. HOD Test",
        initials=Initials("HDT"),
        email=hod_user.email,
    )

    faculty_users: list[User] = []
    faculty_profiles: list[FacultyProfile] = []
    for i in range(3):
        fid = uuid4()
        user = User(
            id=fid,
            email=f"fac_{tag}_{i}@facultydesk.local",
            password_hash=hash_password("Pass123!"),
            role=Role.FACULTY,
            is_active=True,
        )
        profile = FacultyProfile(
            id=uuid4(),
            user_id=fid,
            department_id=dept_id,
            full_name=f"Faculty Member {i}",
            initials=Initials(f"FM{chr(65+i)}"),
            email=user.email,
        )
        faculty_users.append(user)
        faculty_profiles.append(profile)

    async with uow:
        await uow.departments.save(dept)
        await uow.users.save(hod_user)
        await uow.faculty_profiles.save(hod_profile)
        for u, p in zip(faculty_users, faculty_profiles, strict=True):
            await uow.users.save(u)
            await uow.faculty_profiles.save(p)
        await uow.commit()

    template = TaskTemplate(
        id=uuid4(),
        department_id=dept_id,
        title="CO-PO mapping",
        description="Map Course Outcomes to Program Outcomes",
        category=TaskCategory.ACADEMIC_DOCUMENTATION,
        default_lead_days=14,
        default_importance=4,
    )
    async with uow:
        await uow.task_templates.save(template)
        await uow.commit()

    list_tpl_uc = ListTaskTemplatesUseCase(uow)
    async with uow:
        templates = await list_tpl_uc.execute(dept_id)
        assert any(t.title == "CO-PO mapping" for t in templates)

    deadline_utc = now_utc + timedelta(days=5)
    assign_uc = AssignTaskUseCase(uow, clock)
    target_assignee_ids = [u.id for u in faculty_users]

    async with uow:
        assigned_tasks = await assign_uc.execute(
            assigner_id=hod_id,
            title=template.title,
            description=template.description,
            deadline_utc=deadline_utc,
            importance=template.default_importance,
            category=template.category,
            assignee_ids=target_assignee_ids,
        )
        await uow.commit()

    assert len(assigned_tasks) == 3
    parent_assignment_id = assigned_tasks[0].parent_assignment_id
    assert parent_assignment_id is not None
    assert all(t.parent_assignment_id == parent_assignment_id for t in assigned_tasks)

    for task in assigned_tasks:
        async with uow:
            event = await uow.events.get_by_source_id(task.id)
            assert event is not None
            assert event.title == f"Deadline: {task.title}"
            assert event.end_utc == deadline_utc

            notifs = await uow.notifications.list_by_target(task.id)
            assert len(notifs) == 3
            assert all(n.status == NotificationStatus.PENDING for n in notifs)


@pytest.mark.asyncio
async def test_task_priority_sorting_and_completion_cancels_alerts() -> None:
    now_utc = datetime(2026, 10, 28, 12, 0, tzinfo=UTC)
    clock = FrozenClock(now_utc)
    uow = SqlAlchemyUnitOfWork(async_session_factory)

    tag = uuid4().hex[:6]
    user_id = uuid4()
    user = User(
        id=user_id,
        email=f"priority_{tag}@facultydesk.local",
        password_hash=hash_password("Pass123!"),
        role=Role.FACULTY,
        is_active=True,
    )

    async with uow:
        await uow.users.save(user)
        await uow.commit()

    create_uc = CreateTaskUseCase(uow, clock)

    async with uow:
        task_overdue = await create_uc.execute(
            user_id=user_id,
            title="Overdue Accreditation Report",
            description="",
            deadline_utc=now_utc - timedelta(days=2),
            importance=3,
            category=TaskCategory.ACCREDITATION,
        )
        task_urgent = await create_uc.execute(
            user_id=user_id,
            title="Urgent IA Marks Upload",
            description="",
            deadline_utc=now_utc + timedelta(hours=6),
            importance=5,
            category=TaskCategory.EXAM_WORK,
        )
        task_future = await create_uc.execute(
            user_id=user_id,
            title="Lab Manual Preparation",
            description="",
            deadline_utc=now_utc + timedelta(days=10),
            importance=2,
            category=TaskCategory.ACADEMIC_DOCUMENTATION,
        )
        await uow.commit()

    list_uc = ListTasksUseCase(uow, clock)
    async with uow:
        ranked = await list_uc.execute(user_id)

    assert len(ranked) == 3
    assert ranked[0].task.id == task_overdue.id
    assert ranked[0].priority_score > 1.0
    assert ranked[1].task.id == task_urgent.id
    assert 0.0 <= ranked[1].priority_score <= 1.0
    assert ranked[2].task.id == task_future.id
    assert ranked[1].priority_score > ranked[2].priority_score

    complete_uc = CompleteTaskUseCase(uow)
    async with uow:
        completed = await complete_uc.execute(task_urgent.id, user_id)
        assert completed.status == TaskStatus.DONE
        await uow.commit()

        pending_after = await uow.notifications.list_by_target(task_urgent.id)
        assert all(n.status == NotificationStatus.CANCELLED for n in pending_after)

    reopen_uc = ReopenTaskUseCase(uow, clock)
    async with uow:
        reopened = await reopen_uc.execute(task_urgent.id, user_id)
        assert reopened.status == TaskStatus.TODO
        await uow.commit()

        active_notifs = [
            n for n in await uow.notifications.list_by_target(task_urgent.id)
            if n.status == NotificationStatus.PENDING
        ]
        assert len(active_notifs) > 0


@pytest.mark.asyncio
async def test_hod_dashboard_aggregation() -> None:
    now_utc = datetime(2026, 10, 28, 14, 0, tzinfo=UTC)
    clock = FrozenClock(now_utc)
    uow = SqlAlchemyUnitOfWork(async_session_factory)

    tag = uuid4().hex[:6]
    dept_id = uuid4()
    dept = Department(id=dept_id, code=f"H{tag[:3].upper()}", name="HOD Dashboard Dept")

    hod_id = uuid4()
    hod_user = User(
        id=hod_id,
        email=f"hod_dash_{tag}@facultydesk.local",
        password_hash=hash_password("Pass123!"),
        role=Role.HOD,
        is_active=True,
    )
    hod_profile = FacultyProfile(
        id=uuid4(),
        user_id=hod_id,
        department_id=dept_id,
        full_name="Dr. Dashboard HOD",
        initials=Initials("DHD"),
        email=hod_user.email,
    )

    fac1_id = uuid4()
    fac1_user = User(
        id=fac1_id,
        email=f"dash_fac1_{tag}@facultydesk.local",
        password_hash=hash_password("Pass123!"),
        role=Role.FACULTY,
        is_active=True,
    )
    fac1_profile = FacultyProfile(
        id=uuid4(),
        user_id=fac1_id,
        department_id=dept_id,
        full_name="Prof. One",
        initials=Initials("PONE"),
        email=fac1_user.email,
    )

    fac2_id = uuid4()
    fac2_user = User(
        id=fac2_id,
        email=f"dash_fac2_{tag}@facultydesk.local",
        password_hash=hash_password("Pass123!"),
        role=Role.FACULTY,
        is_active=True,
    )
    fac2_profile = FacultyProfile(
        id=uuid4(),
        user_id=fac2_id,
        department_id=dept_id,
        full_name="Prof. Two",
        initials=Initials("PTWO"),
        email=fac2_user.email,
    )

    async with uow:
        await uow.departments.save(dept)
        await uow.users.save(hod_user)
        await uow.faculty_profiles.save(hod_profile)
        await uow.users.save(fac1_user)
        await uow.faculty_profiles.save(fac1_profile)
        await uow.users.save(fac2_user)
        await uow.faculty_profiles.save(fac2_profile)
        await uow.commit()

    assign_uc = AssignTaskUseCase(uow, clock)
    complete_uc = CompleteTaskUseCase(uow)

    async with uow:
        assigned = await assign_uc.execute(
            assigner_id=hod_id,
            title="Bulk Attendance Shortage",
            description="",
            deadline_utc=now_utc - timedelta(days=1),
            importance=4,
            category=TaskCategory.ACADEMIC_DOCUMENTATION,
            assignee_ids=[fac1_id, fac2_id],
        )
        await uow.commit()

        await complete_uc.execute(assigned[0].id, fac1_id)
        await uow.commit()

    dashboard_uc = GetHodDashboardUseCase(uow, clock)
    async with uow:
        dash = await dashboard_uc.execute(department_id=dept_id)

    assert dash.total_assigned == 2
    assert dash.total_completed == 1
    assert dash.overall_completion_rate == 50.0
    assert dash.total_overdue == 1

    f2_summary = next(f for f in dash.faculty_overdue if f.user_id == fac2_id)
    assert f2_summary.overdue_count == 1
    f1_summary = next(f for f in dash.faculty_overdue if f.user_id == fac1_id)
    assert f1_summary.overdue_count == 0
