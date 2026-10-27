from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from app.application.tasks.maths import (
    compute_completion_rate,
    compute_lead_alert_times,
    compute_priority_score,
)
from app.core.clock import Clock
from app.domain import (
    AttendeeResponse,
    DomainError,
    EntityNotFound,
    Event,
    EventAttendee,
    EventKind,
    EventSource,
    NotificationChannel,
    NotificationStatus,
    ScheduledNotification,
    Task,
    TaskCategory,
    TaskRecurrence,
    TaskStatus,
    TaskTemplate,
    UnitOfWork,
)


@dataclass(frozen=True)
class TaskWithScore:
    task: Task
    priority_score: float


@dataclass(frozen=True)
class AssignmentProgress:
    assignment_id: UUID
    title: str
    category: TaskCategory
    total_count: int
    completed_count: int
    completion_rate: float


@dataclass(frozen=True)
class FacultyOverdueSummary:
    user_id: UUID
    faculty_id: UUID | None
    faculty_name: str
    email: str
    overdue_count: int


@dataclass(frozen=True)
class HodDashboardData:
    assignments: list[AssignmentProgress]
    faculty_overdue: list[FacultyOverdueSummary]
    overall_completion_rate: float
    total_assigned: int
    total_completed: int
    total_overdue: int


class CreateTaskUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        user_id: UUID,
        title: str,
        description: str,
        deadline_utc: datetime,
        importance: int = 3,
        category: TaskCategory = TaskCategory.ACADEMIC_DOCUMENTATION,
        recurrence: TaskRecurrence | None = None,
    ) -> Task:
        now = self._clock.now()
        task = Task(
            id=uuid4(),
            title=title,
            description=description,
            deadline_utc=deadline_utc,
            importance=importance,
            category=category,
            status=TaskStatus.TODO,
            assignee_id=user_id,
            assigner_id=user_id,
            parent_assignment_id=None,
            recurrence=recurrence,
            created_at_utc=now,
        )
        saved_task = await self._uow.tasks.save(task)

        profile = await self._uow.faculty_profiles.get_by_user_id(user_id)
        attendees = (
            [
                EventAttendee(
                    event_id=uuid4(),
                    faculty_id=profile.id,
                    response=AttendeeResponse.ACCEPTED,
                )
            ]
            if profile is not None
            else []
        )
        deadline_event = Event(
            id=uuid4(),
            kind=EventKind.DEADLINE,
            title=f"Deadline: {saved_task.title}",
            start_utc=saved_task.deadline_utc - timedelta(minutes=15),
            end_utc=saved_task.deadline_utc,
            location="",
            source=EventSource.TASK,
            source_id=saved_task.id,
            attendees=attendees,
        )
        await self._uow.events.save(deadline_event)

        lead_times = compute_lead_alert_times(
            deadline_utc=saved_task.deadline_utc,
            created_at_utc=now,
        )
        for fire_time in lead_times:
            hours_offset = int((saved_task.deadline_utc - fire_time).total_seconds() // 3600)
            idempotency_key = f"task:{saved_task.id}:lead:{hours_offset}h:{fire_time.isoformat()}"
            notification = ScheduledNotification(
                id=uuid4(),
                target_id=saved_task.id,
                target_kind="TASK",
                user_id=saved_task.assignee_id,
                channel=NotificationChannel.EMAIL,
                fire_at_utc=fire_time,
                idempotency_key=idempotency_key,
                status=NotificationStatus.PENDING,
            )
            await self._uow.notifications.save(notification)

        return saved_task


class AssignTaskUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        assigner_id: UUID,
        title: str,
        description: str,
        deadline_utc: datetime,
        importance: int = 3,
        category: TaskCategory = TaskCategory.ACADEMIC_DOCUMENTATION,
        recurrence: TaskRecurrence | None = None,
        assignee_ids: list[UUID] | None = None,
        department_id: UUID | None = None,
    ) -> list[Task]:
        target_user_ids: list[UUID] = []
        if assignee_ids:
            for aid in assignee_ids:
                prof = await self._uow.faculty_profiles.get_by_id(aid)
                if prof is not None:
                    target_user_ids.append(prof.user_id)
                else:
                    target_user_ids.append(aid)
        elif department_id is not None:
            profiles = await self._uow.faculty_profiles.list_by_department(department_id)
            target_user_ids.extend([p.user_id for p in profiles])

        if not target_user_ids:
            raise DomainError("No assignees specified for task assignment")

        unique_user_ids = list(dict.fromkeys(target_user_ids))
        now = self._clock.now()
        parent_assignment_id = uuid4()
        created_tasks: list[Task] = []

        for uid in unique_user_ids:
            task = Task(
                id=uuid4(),
                title=title,
                description=description,
                deadline_utc=deadline_utc,
                importance=importance,
                category=category,
                status=TaskStatus.TODO,
                assignee_id=uid,
                assigner_id=assigner_id,
                parent_assignment_id=parent_assignment_id,
                recurrence=recurrence,
                created_at_utc=now,
            )
            saved_task = await self._uow.tasks.save(task)
            created_tasks.append(saved_task)

            profile = await self._uow.faculty_profiles.get_by_user_id(uid)
            attendees = (
                [
                    EventAttendee(
                        event_id=uuid4(),
                        faculty_id=profile.id,
                        response=AttendeeResponse.ACCEPTED,
                    )
                ]
                if profile is not None
                else []
            )
            deadline_event = Event(
                id=uuid4(),
                kind=EventKind.DEADLINE,
                title=f"Deadline: {saved_task.title}",
                start_utc=saved_task.deadline_utc - timedelta(minutes=15),
                end_utc=saved_task.deadline_utc,
                location="",
                source=EventSource.TASK,
                source_id=saved_task.id,
                attendees=attendees,
            )
            await self._uow.events.save(deadline_event)

            lead_times = compute_lead_alert_times(
                deadline_utc=saved_task.deadline_utc,
                created_at_utc=now,
            )
            for fire_time in lead_times:
                hours_offset = int((saved_task.deadline_utc - fire_time).total_seconds() // 3600)
                iso = fire_time.isoformat()
                idempotency_key = f"task:{saved_task.id}:lead:{hours_offset}h:{iso}"
                notification = ScheduledNotification(
                    id=uuid4(),
                    target_id=saved_task.id,
                    target_kind="TASK",
                    user_id=saved_task.assignee_id,
                    channel=NotificationChannel.EMAIL,
                    fire_at_utc=fire_time,
                    idempotency_key=idempotency_key,
                    status=NotificationStatus.PENDING,
                )
                await self._uow.notifications.save(notification)

        return created_tasks


class UpdateTaskUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        task_id: UUID,
        user_id: UUID,
        title: str | None = None,
        description: str | None = None,
        deadline_utc: datetime | None = None,
        importance: int | None = None,
        category: TaskCategory | None = None,
        recurrence: TaskRecurrence | None = None,
    ) -> Task:
        task = await self._uow.tasks.get_by_id(task_id)
        if task is None:
            raise EntityNotFound("Task", str(task_id))

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if importance is not None:
            task.importance = importance
        if category is not None:
            task.category = category
        if recurrence is not None:
            task.recurrence = recurrence

        now = self._clock.now()
        if deadline_utc is not None and deadline_utc != task.deadline_utc:
            task.update_deadline(deadline_utc)
            event = await self._uow.events.get_by_source_id(task.id)
            if event is not None:
                event.start_utc = deadline_utc - timedelta(minutes=15)
                event.end_utc = deadline_utc
                event.title = f"Deadline: {task.title}"
                await self._uow.events.save(event)

            await self._uow.notifications.cancel_pending_by_target(task.id)
            lead_times = compute_lead_alert_times(
                deadline_utc=deadline_utc,
                created_at_utc=now,
            )
            for fire_time in lead_times:
                hours_offset = int((deadline_utc - fire_time).total_seconds() // 3600)
                iso = fire_time.isoformat()
                ts = int(now.timestamp())
                idempotency_key = f"task:{task.id}:update:{ts}:{hours_offset}h:{iso}"
                notification = ScheduledNotification(
                    id=uuid4(),
                    target_id=task.id,
                    target_kind="TASK",
                    user_id=task.assignee_id,
                    channel=NotificationChannel.EMAIL,
                    fire_at_utc=fire_time,
                    idempotency_key=idempotency_key,
                    status=NotificationStatus.PENDING,
                )
                await self._uow.notifications.save(notification)
        elif title is not None:
            event = await self._uow.events.get_by_source_id(task.id)
            if event is not None:
                event.title = f"Deadline: {task.title}"
                await self._uow.events.save(event)

        return await self._uow.tasks.save(task)


class CompleteTaskUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, task_id: UUID, user_id: UUID) -> Task:
        task = await self._uow.tasks.get_by_id(task_id)
        if task is None:
            raise EntityNotFound("Task", str(task_id))

        task.change_status(TaskStatus.DONE)
        saved = await self._uow.tasks.save(task)
        await self._uow.notifications.cancel_pending_by_target(task.id)
        return saved


class ReopenTaskUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(self, task_id: UUID, user_id: UUID) -> Task:
        task = await self._uow.tasks.get_by_id(task_id)
        if task is None:
            raise EntityNotFound("Task", str(task_id))

        task.change_status(TaskStatus.TODO)
        saved = await self._uow.tasks.save(task)

        now = self._clock.now()
        if task.deadline_utc > now:
            lead_times = compute_lead_alert_times(
                deadline_utc=task.deadline_utc,
                created_at_utc=now,
            )
            for fire_time in lead_times:
                hours_offset = int((task.deadline_utc - fire_time).total_seconds() // 3600)
                iso = fire_time.isoformat()
                ts = int(now.timestamp())
                idempotency_key = f"task:{task.id}:reopen:{ts}:{hours_offset}h:{iso}"
                notification = ScheduledNotification(
                    id=uuid4(),
                    target_id=task.id,
                    target_kind="TASK",
                    user_id=task.assignee_id,
                    channel=NotificationChannel.EMAIL,
                    fire_at_utc=fire_time,
                    idempotency_key=idempotency_key,
                    status=NotificationStatus.PENDING,
                )
                await self._uow.notifications.save(notification)

        return saved


class DeleteTaskUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, task_id: UUID, user_id: UUID) -> None:
        task = await self._uow.tasks.get_by_id(task_id)
        if task is None:
            raise EntityNotFound("Task", str(task_id))

        if task.assignee_id != user_id and task.assigner_id != user_id:
            raise DomainError("Cannot delete another user's task")

        if task.parent_assignment_id is not None and task.assigner_id != user_id:
            raise DomainError("Cannot delete an assigned task; only the assigner may delete it")

        await self._uow.notifications.cancel_pending_by_target(task.id)
        await self._uow.events.delete_by_source_id(task.id)
        await self._uow.tasks.delete(task.id)


class ListTasksUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        user_id: UUID,
        status: TaskStatus | None = None,
    ) -> list[TaskWithScore]:
        tasks = await self._uow.tasks.list_by_assignee(user_id, status=status)
        now = self._clock.now()
        scored: list[TaskWithScore] = []
        for task in tasks:
            score = compute_priority_score(
                importance=task.importance,
                deadline_utc=task.deadline_utc,
                now_utc=now,
                is_completed=(task.status == TaskStatus.DONE),
            )
            scored.append(TaskWithScore(task=task, priority_score=score))

        scored.sort(key=lambda item: item.priority_score, reverse=True)
        return scored


class GetHodDashboardUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        department_id: UUID | None = None,
        assigner_id: UUID | None = None,
    ) -> HodDashboardData:
        now = self._clock.now()
        all_tasks = await self._uow.tasks.list_all()

        profiles_by_user_id: dict[UUID, tuple[UUID, str, str]] = {}
        if department_id is not None:
            profiles = await self._uow.faculty_profiles.list_by_department(department_id)
            for p in profiles:
                profiles_by_user_id[p.user_id] = (p.id, p.full_name, p.email)

        filtered_tasks: list[Task] = []
        for task in all_tasks:
            if department_id is not None and task.assignee_id not in profiles_by_user_id:
                continue
            if assigner_id is not None and task.assigner_id != assigner_id:
                continue
            filtered_tasks.append(task)

        parent_groups: dict[UUID, list[Task]] = {}
        for task in filtered_tasks:
            group_key = task.parent_assignment_id or task.id
            parent_groups.setdefault(group_key, []).append(task)

        assignments: list[AssignmentProgress] = []
        for group_id, group_tasks in parent_groups.items():
            total = len(group_tasks)
            completed = sum(1 for t in group_tasks if t.status == TaskStatus.DONE)
            rate = compute_completion_rate(total_tasks=total, completed_tasks=completed)
            first_task = group_tasks[0]
            assignments.append(
                AssignmentProgress(
                    assignment_id=group_id,
                    title=first_task.title,
                    category=first_task.category,
                    total_count=total,
                    completed_count=completed,
                    completion_rate=rate,
                )
            )

        overdue_counts: dict[UUID, int] = {}
        for task in filtered_tasks:
            if task.status != TaskStatus.DONE and task.deadline_utc < now:
                overdue_counts[task.assignee_id] = overdue_counts.get(task.assignee_id, 0) + 1

        faculty_overdue: list[FacultyOverdueSummary] = []
        target_uids = (
            set(profiles_by_user_id.keys())
            if department_id is not None
            else {t.assignee_id for t in filtered_tasks}
        )

        for uid in target_uids:
            cnt = overdue_counts.get(uid, 0)
            if uid in profiles_by_user_id:
                fid, fname, femail = profiles_by_user_id[uid]
            else:
                user = await self._uow.users.get_by_id(uid)
                fid = None
                fname = user.email if user else str(uid)
                femail = user.email if user else ""

            faculty_overdue.append(
                FacultyOverdueSummary(
                    user_id=uid,
                    faculty_id=fid,
                    faculty_name=fname,
                    email=femail,
                    overdue_count=cnt,
                )
            )

        faculty_overdue.sort(key=lambda f: f.overdue_count, reverse=True)

        total_assigned = len(filtered_tasks)
        total_completed = sum(1 for t in filtered_tasks if t.status == TaskStatus.DONE)
        total_overdue = sum(overdue_counts.values())
        overall_rate = compute_completion_rate(
            total_tasks=total_assigned, completed_tasks=total_completed
        )

        return HodDashboardData(
            assignments=assignments,
            faculty_overdue=faculty_overdue,
            overall_completion_rate=overall_rate,
            total_assigned=total_assigned,
            total_completed=total_completed,
            total_overdue=total_overdue,
        )


class ListTaskTemplatesUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, department_id: UUID | None = None) -> list[TaskTemplate]:
        return await self._uow.task_templates.list_by_department(department_id)
