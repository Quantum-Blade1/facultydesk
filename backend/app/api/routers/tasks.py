from datetime import UTC, datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Query, Response, status
from pydantic import BaseModel, Field

from app.api.deps import get_clock, get_current_principal, get_uow
from app.application.security.policy import Principal
from app.application.tasks.maths import compute_priority_score
from app.application.tasks.use_cases import (
    AssignTaskUseCase,
    CompleteTaskUseCase,
    CreateTaskUseCase,
    DeleteTaskUseCase,
    GetHodDashboardUseCase,
    ListTasksUseCase,
    ListTaskTemplatesUseCase,
    ReopenTaskUseCase,
    UpdateTaskUseCase,
)
from app.core.clock import Clock
from app.core.errors import ForbiddenError, NotFoundError
from app.domain import (
    EntityNotFound,
    Role,
    Task,
    TaskCategory,
    TaskRecurrence,
    TaskStatus,
    TaskTemplate,
    UnitOfWork,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


def ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=ZoneInfo("Asia/Kolkata")).astimezone(UTC)
    return dt.astimezone(UTC)


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="")
    deadline: datetime
    importance: int = Field(default=3, ge=1, le=5)
    category: TaskCategory = TaskCategory.ACADEMIC_DOCUMENTATION
    recurrence: TaskRecurrence | None = None


class AssignTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="")
    deadline: datetime
    importance: int = Field(default=3, ge=1, le=5)
    category: TaskCategory = TaskCategory.ACADEMIC_DOCUMENTATION
    recurrence: TaskRecurrence | None = None
    assignee_ids: list[UUID] = Field(default_factory=list)
    department_id: UUID | None = None


class UpdateTaskRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    deadline: datetime | None = None
    importance: int | None = Field(default=None, ge=1, le=5)
    category: TaskCategory | None = None
    recurrence: TaskRecurrence | None = None


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str
    deadline_utc: str
    importance: int
    category: str
    status: str
    assignee_id: UUID
    assigner_id: UUID
    parent_assignment_id: UUID | None
    recurrence: str | None
    created_at_utc: str
    priority_score: float

    @classmethod
    def from_domain(cls, task: Task, priority_score: float) -> "TaskResponse":
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            deadline_utc=task.deadline_utc.isoformat(),
            importance=task.importance,
            category=task.category.value,
            status=task.status.value,
            assignee_id=task.assignee_id,
            assigner_id=task.assigner_id,
            parent_assignment_id=task.parent_assignment_id,
            recurrence=task.recurrence.value if task.recurrence else None,
            created_at_utc=task.created_at_utc.isoformat(),
            priority_score=priority_score,
        )


class TaskTemplateResponse(BaseModel):
    id: UUID
    department_id: UUID | None
    title: str
    description: str
    category: str
    default_lead_days: int
    default_importance: int

    @classmethod
    def from_domain(cls, tpl: TaskTemplate) -> "TaskTemplateResponse":
        return cls(
            id=tpl.id,
            department_id=tpl.department_id,
            title=tpl.title,
            description=tpl.description,
            category=tpl.category.value,
            default_lead_days=tpl.default_lead_days,
            default_importance=tpl.default_importance,
        )


class AssignmentProgressResponse(BaseModel):
    assignment_id: UUID
    title: str
    category: str
    total_count: int
    completed_count: int
    completion_rate: float


class FacultyOverdueSummaryResponse(BaseModel):
    user_id: UUID
    faculty_id: UUID | None
    faculty_name: str
    email: str
    overdue_count: int


class HodDashboardResponse(BaseModel):
    assignments: list[AssignmentProgressResponse]
    faculty_overdue: list[FacultyOverdueSummaryResponse]
    overall_completion_rate: float
    total_assigned: int
    total_completed: int
    total_overdue: int


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    body: CreateTaskRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> TaskResponse:
    """Create a personal documentation task with deadline reminders and calendar event."""
    deadline_utc = ensure_utc(body.deadline)
    use_case = CreateTaskUseCase(uow, clock)
    async with uow:
        task = await use_case.execute(
            user_id=principal.user_id,
            title=body.title,
            description=body.description,
            deadline_utc=deadline_utc,
            importance=body.importance,
            category=body.category,
            recurrence=body.recurrence,
        )
        await uow.commit()

    score = compute_priority_score(
        importance=task.importance,
        deadline_utc=task.deadline_utc,
        now_utc=clock.now(),
        is_completed=False,
    )
    return TaskResponse.from_domain(task, score)


@router.post("/assign", response_model=list[TaskResponse], status_code=status.HTTP_201_CREATED)
async def assign_task(
    body: AssignTaskRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> list[TaskResponse]:
    """HOD or Admin assigns a task to one faculty, multiple faculty, or department."""
    if principal.role not in (Role.HOD, Role.ADMIN):
        raise ForbiddenError("Only HOD or Admin can bulk assign tasks")

    dept_id = body.department_id or principal.department_id
    deadline_utc = ensure_utc(body.deadline)
    use_case = AssignTaskUseCase(uow, clock)

    async with uow:
        tasks = await use_case.execute(
            assigner_id=principal.user_id,
            title=body.title,
            description=body.description,
            deadline_utc=deadline_utc,
            importance=body.importance,
            category=body.category,
            recurrence=body.recurrence,
            assignee_ids=body.assignee_ids,
            department_id=dept_id,
        )
        await uow.commit()

    now = clock.now()
    responses: list[TaskResponse] = []
    for t in tasks:
        score = compute_priority_score(
            importance=t.importance,
            deadline_utc=t.deadline_utc,
            now_utc=now,
            is_completed=False,
        )
        responses.append(TaskResponse.from_domain(t, score))
    return responses


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> list[TaskResponse]:
    """List tasks assigned to the current user, ranked descending by Priority Score P."""
    use_case = ListTasksUseCase(uow, clock)
    async with uow:
        scored = await use_case.execute(principal.user_id, status=status_filter)

    return [TaskResponse.from_domain(item.task, item.priority_score) for item in scored]


@router.get("/templates", response_model=list[TaskTemplateResponse])
async def list_templates(
    department_id: UUID | None = Query(default=None),
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> list[TaskTemplateResponse]:
    """List available task templates for quick assignment."""
    target_dept_id = department_id or principal.department_id
    use_case = ListTaskTemplatesUseCase(uow)
    async with uow:
        templates = await use_case.execute(target_dept_id)

    return [TaskTemplateResponse.from_domain(tpl) for tpl in templates]


@router.get("/hod-dashboard", response_model=HodDashboardResponse)
async def get_hod_dashboard(
    department_id: UUID | None = Query(default=None),
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> HodDashboardResponse:
    """Retrieve HOD dashboard metrics: assignment completion rates and faculty overdue counts."""
    if principal.role not in (Role.HOD, Role.ADMIN):
        raise ForbiddenError("Only HOD or Admin can view the dashboard")

    target_dept_id = department_id or principal.department_id
    use_case = GetHodDashboardUseCase(uow, clock)
    async with uow:
        data = await use_case.execute(department_id=target_dept_id)

    return HodDashboardResponse(
        assignments=[
            AssignmentProgressResponse(
                assignment_id=a.assignment_id,
                title=a.title,
                category=a.category.value,
                total_count=a.total_count,
                completed_count=a.completed_count,
                completion_rate=a.completion_rate,
            )
            for a in data.assignments
        ],
        faculty_overdue=[
            FacultyOverdueSummaryResponse(
                user_id=f.user_id,
                faculty_id=f.faculty_id,
                faculty_name=f.faculty_name,
                email=f.email,
                overdue_count=f.overdue_count,
            )
            for f in data.faculty_overdue
        ],
        overall_completion_rate=data.overall_completion_rate,
        total_assigned=data.total_assigned,
        total_completed=data.total_completed,
        total_overdue=data.total_overdue,
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> TaskResponse:
    """Get single task by ID."""
    async with uow:
        task = await uow.tasks.get_by_id(task_id)

    if task is None:
        raise NotFoundError(f"Task {task_id} not found")

    if principal.role == Role.FACULTY and task.assignee_id != principal.user_id:
        raise ForbiddenError("Cannot view another faculty member's task")

    score = compute_priority_score(
        importance=task.importance,
        deadline_utc=task.deadline_utc,
        now_utc=clock.now(),
        is_completed=(task.status == TaskStatus.DONE),
    )
    return TaskResponse.from_domain(task, score)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    body: UpdateTaskRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> TaskResponse:
    """Update task details and reschedule deadline reminders."""
    deadline_utc = ensure_utc(body.deadline) if body.deadline is not None else None
    use_case = UpdateTaskUseCase(uow, clock)

    async with uow:
        task = await uow.tasks.get_by_id(task_id)
        if task is None:
            raise NotFoundError(f"Task {task_id} not found")
        if principal.role == Role.FACULTY and task.assignee_id != principal.user_id:
            raise ForbiddenError("Cannot edit another faculty member's task")

        updated = await use_case.execute(
            task_id=task_id,
            user_id=principal.user_id,
            title=body.title,
            description=body.description,
            deadline_utc=deadline_utc,
            importance=body.importance,
            category=body.category,
            recurrence=body.recurrence,
        )
        await uow.commit()

    score = compute_priority_score(
        importance=updated.importance,
        deadline_utc=updated.deadline_utc,
        now_utc=clock.now(),
        is_completed=(updated.status == TaskStatus.DONE),
    )
    return TaskResponse.from_domain(updated, score)


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: UUID,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> TaskResponse:
    """Mark a task as completed and cancel all its pending alerts."""
    use_case = CompleteTaskUseCase(uow)
    async with uow:
        task = await uow.tasks.get_by_id(task_id)
        if task is None:
            raise NotFoundError(f"Task {task_id} not found")
        if principal.role == Role.FACULTY and task.assignee_id != principal.user_id:
            raise ForbiddenError("Cannot complete another faculty member's task")

        completed = await use_case.execute(task_id, principal.user_id)
        await uow.commit()

    score = compute_priority_score(
        importance=completed.importance,
        deadline_utc=completed.deadline_utc,
        now_utc=clock.now(),
        is_completed=True,
    )
    return TaskResponse.from_domain(completed, score)


@router.post("/{task_id}/reopen", response_model=TaskResponse)
async def reopen_task(
    task_id: UUID,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> TaskResponse:
    """Reopen a completed task."""
    use_case = ReopenTaskUseCase(uow, clock)
    async with uow:
        task = await uow.tasks.get_by_id(task_id)
        if task is None:
            raise NotFoundError(f"Task {task_id} not found")
        if principal.role == Role.FACULTY and task.assignee_id != principal.user_id:
            raise ForbiddenError("Cannot reopen another faculty member's task")

        reopened = await use_case.execute(task_id, principal.user_id)
        await uow.commit()

    score = compute_priority_score(
        importance=reopened.importance,
        deadline_utc=reopened.deadline_utc,
        now_utc=clock.now(),
        is_completed=False,
    )
    return TaskResponse.from_domain(reopened, score)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> Response:
    """Delete own unassigned task or assigned task by assigner."""
    use_case = DeleteTaskUseCase(uow)
    async with uow:
        try:
            await use_case.execute(task_id, principal.user_id)
            await uow.commit()
        except EntityNotFound as err:
            raise NotFoundError(f"Task {task_id} not found") from err

    return Response(status_code=status.HTTP_204_NO_CONTENT)
