from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Self
from uuid import UUID

from app.domain.entities import (
    AcademicTerm,
    AuditLog,
    Circular,
    Course,
    Department,
    Event,
    FacultyProfile,
    Holiday,
    PushSubscription,
    RefreshToken,
    ReminderRule,
    Room,
    ScheduledNotification,
    Section,
    Task,
    TaskTemplate,
    TimetableSlot,
    TimetableUpload,
    User,
)
from app.domain.value_objects import EventKind, Initials, NotificationStatus, TaskStatus


class DepartmentRepository(ABC):
    @abstractmethod
    async def get_by_id(self, department_id: UUID) -> Department | None:
        """Fetch department by unique identifier."""

    @abstractmethod
    async def get_by_code(self, code: str) -> Department | None:
        """Fetch department by its unique code."""

    @abstractmethod
    async def list_all(self) -> list[Department]:
        """List all departments."""

    @abstractmethod
    async def save(self, department: Department) -> Department:
        """Persist a department."""


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        """Fetch user by unique identifier."""

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Fetch user by unique email."""

    @abstractmethod
    async def save(self, user: User) -> User:
        """Persist a user."""


class FacultyProfileRepository(ABC):
    @abstractmethod
    async def get_by_id(self, profile_id: UUID) -> FacultyProfile | None:
        """Fetch faculty profile by unique identifier."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> FacultyProfile | None:
        """Fetch faculty profile by user identifier."""

    @abstractmethod
    async def get_by_department_and_initials(
        self, department_id: UUID, initials: Initials
    ) -> FacultyProfile | None:
        """Fetch faculty profile by department and unique initials."""

    @abstractmethod
    async def list_by_department(self, department_id: UUID) -> list[FacultyProfile]:
        """List all faculty profiles in a department."""

    @abstractmethod
    async def list_all(self) -> list[FacultyProfile]:
        """List all faculty profiles across departments."""

    @abstractmethod
    async def get_by_ics_token(self, token: str) -> FacultyProfile | None:
        """Fetch faculty profile by unique ICS subscription token."""

    @abstractmethod
    async def save(self, profile: FacultyProfile) -> FacultyProfile:
        """Persist a faculty profile."""


class AcademicTermRepository(ABC):
    @abstractmethod
    async def get_by_id(self, term_id: UUID) -> AcademicTerm | None:
        """Fetch academic term by unique identifier."""

    @abstractmethod
    async def get_active_term(self, on_date: date) -> AcademicTerm | None:
        """Fetch the active term containing the given calendar date."""

    @abstractmethod
    async def save(self, term: AcademicTerm) -> AcademicTerm:
        """Persist an academic term."""

    @abstractmethod
    async def list_all(self) -> list[AcademicTerm]:
        """List all academic terms."""

    @abstractmethod
    async def list_holidays(self, term_id: UUID) -> list[Holiday]:
        """List holidays scheduled within a term."""

    @abstractmethod
    async def list_all_holidays(self) -> list[Holiday]:
        """List all holidays across all terms."""

    @abstractmethod
    async def save_holiday(self, holiday: Holiday) -> Holiday:
        """Persist a holiday."""


class EventRepository(ABC):
    @abstractmethod
    async def get_by_id(self, event_id: UUID) -> Event | None:
        """Fetch scheduled event by unique identifier."""

    @abstractmethod
    async def list_by_faculty_and_range(
        self, faculty_id: UUID, start_utc: datetime, end_utc: datetime
    ) -> list[Event]:
        """List events for a faculty member within the half-open UTC interval."""

    @abstractmethod
    async def save(self, event: Event) -> Event:
        """Persist an event along with attendee relationships."""

    @abstractmethod
    async def delete(self, event_id: UUID) -> None:
        """Remove an event by its identifier."""

    @abstractmethod
    async def get_by_slot_and_date(self, slot_id: UUID, recurrence_date: date) -> Event | None:
        """Fetch event by timetable slot identifier and occurrence date."""

    @abstractmethod
    async def delete_future_by_slot(self, slot_id: UUID, from_date: date) -> None:
        """Delete future materialised timetable occurrences for a slot."""

    @abstractmethod
    async def get_by_source_id(self, source_id: UUID) -> Event | None:
        """Fetch event by source ID."""

    @abstractmethod
    async def delete_by_source_id(self, source_id: UUID) -> None:
        """Delete event by source ID."""


class CircularRepository(ABC):
    @abstractmethod
    async def get_by_id(self, circular_id: UUID) -> Circular | None:
        """Fetch circular by unique identifier."""

    @abstractmethod
    async def list_pending_review(self) -> list[Circular]:
        """List circulars currently awaiting human review."""

    @abstractmethod
    async def save(self, circular: Circular) -> Circular:
        """Persist a circular aggregate."""


class NotificationRepository(ABC):
    @abstractmethod
    async def get_by_id(self, notification_id: UUID) -> ScheduledNotification | None:
        """Fetch notification by unique identifier."""

    @abstractmethod
    async def get_by_idempotency_key(self, idempotency_key: str) -> ScheduledNotification | None:
        """Fetch notification by unique idempotency key."""

    @abstractmethod
    async def list_due(self, up_to_utc: datetime) -> list[ScheduledNotification]:
        """List pending notifications due to fire at or before up_to_utc."""

    @abstractmethod
    async def claim_due_batch(self, up_to_utc: datetime, limit: int) -> list[ScheduledNotification]:
        """Claim due notifications via SELECT FOR UPDATE SKIP LOCKED, marking them SENDING."""

    @abstractmethod
    async def recover_stale_sending(self, older_than_utc: datetime) -> int:
        """Transition notifications stuck in SENDING older than threshold back to PENDING."""

    @abstractmethod
    async def list_by_user(
        self, user_id: UUID, status: NotificationStatus | None = None, limit: int = 50
    ) -> list[ScheduledNotification]:
        """List notifications for a user."""

    @abstractmethod
    async def list_by_target(self, target_id: UUID) -> list[ScheduledNotification]:
        """List all notifications for a target event or task."""

    @abstractmethod
    async def cancel_pending_by_target(self, target_id: UUID) -> int:
        """Cancel all pending notifications for a target."""

    @abstractmethod
    async def count_by_status(self) -> dict[str, int]:
        """Return counts of notifications grouped by status."""

    @abstractmethod
    async def list_delivered_lateness_samples(self, limit: int = 5000) -> list[float]:
        """Return sequence of lateness observations in seconds for delivered notifications."""

    @abstractmethod
    async def list_dead_letters(self, limit: int = 50) -> list[ScheduledNotification]:
        """Return list of failed notifications awaiting administrative review or retry."""

    @abstractmethod
    async def save(self, notification: ScheduledNotification) -> ScheduledNotification:
        """Persist a scheduled notification."""


class ReminderRuleRepository(ABC):
    @abstractmethod
    async def get_by_user_and_kind(
        self, user_id: UUID, event_kind: EventKind
    ) -> ReminderRule | None:
        """Fetch reminder rule for a user and event kind."""

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[ReminderRule]:
        """List all reminder rules for a user."""

    @abstractmethod
    async def save(self, rule: ReminderRule) -> ReminderRule:
        """Persist a reminder rule."""

    @abstractmethod
    async def delete(self, rule_id: UUID) -> None:
        """Delete a reminder rule."""


class PushSubscriptionRepository(ABC):
    @abstractmethod
    async def get_by_id(self, subscription_id: UUID) -> PushSubscription | None:
        """Fetch push subscription by ID."""

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[PushSubscription]:
        """List all push subscriptions for a user."""

    @abstractmethod
    async def save(self, subscription: PushSubscription) -> PushSubscription:
        """Persist a push subscription."""

    @abstractmethod
    async def delete_by_endpoint(self, endpoint: str) -> None:
        """Delete push subscription matching endpoint."""

    @abstractmethod
    async def delete(self, subscription_id: UUID) -> None:
        """Delete push subscription."""


class TaskRepository(ABC):
    @abstractmethod
    async def get_by_id(self, task_id: UUID) -> Task | None:
        """Fetch task by unique identifier."""

    @abstractmethod
    async def list_by_assignee(
        self, assignee_id: UUID, status: TaskStatus | None = None
    ) -> list[Task]:
        """List tasks assigned to a user."""

    @abstractmethod
    async def list_by_parent_assignment(self, parent_assignment_id: UUID) -> list[Task]:
        """List all subtasks belonging to a parent bulk assignment."""

    @abstractmethod
    async def list_by_assigner(self, assigner_id: UUID) -> list[Task]:
        """List tasks created/assigned by a user."""

    @abstractmethod
    async def list_overdue(self, as_of_utc: datetime) -> list[Task]:
        """List uncompleted tasks whose deadline has passed."""

    @abstractmethod
    async def list_all(self) -> list[Task]:
        """List all tasks across system."""

    @abstractmethod
    async def save(self, task: Task) -> Task:
        """Persist a task."""

    @abstractmethod
    async def delete(self, task_id: UUID) -> None:
        """Delete a task."""


class TaskTemplateRepository(ABC):
    @abstractmethod
    async def get_by_id(self, template_id: UUID) -> TaskTemplate | None:
        """Fetch template by ID."""

    @abstractmethod
    async def list_by_department(self, department_id: UUID | None) -> list[TaskTemplate]:
        """List templates available to a department, including institute-wide templates."""

    @abstractmethod
    async def save(self, template: TaskTemplate) -> TaskTemplate:
        """Persist a task template."""

    @abstractmethod
    async def delete(self, template_id: UUID) -> None:
        """Delete a task template."""


class AuditLogRepository(ABC):
    @abstractmethod
    async def save(self, audit_log: AuditLog) -> AuditLog:
        """Persist an audit log entry."""

    @abstractmethod
    async def list_by_resource(self, resource_type: str, resource_id: str) -> list[AuditLog]:
        """List audit entries associated with a specific resource."""


class RefreshTokenRepository(ABC):
    @abstractmethod
    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        """Fetch refresh token by its SHA-256 hash."""

    @abstractmethod
    async def save(self, token: RefreshToken) -> RefreshToken:
        """Persist a refresh token record."""

    @abstractmethod
    async def revoke_family(self, family_id: UUID) -> None:
        """Revoke all tokens belonging to a family."""

    @abstractmethod
    async def revoke_all_for_user(self, user_id: UUID) -> None:
        """Revoke all refresh tokens for a user."""


class CourseRepository(ABC):
    @abstractmethod
    async def get_by_id(self, course_id: UUID) -> Course | None:
        """Fetch course by unique identifier."""

    @abstractmethod
    async def get_by_department_and_code(self, department_id: UUID, code: str) -> Course | None:
        """Fetch course by department and course code."""

    @abstractmethod
    async def save(self, course: Course) -> Course:
        """Persist a course."""


class SectionRepository(ABC):
    @abstractmethod
    async def get_by_id(self, section_id: UUID) -> Section | None:
        """Fetch section by unique identifier."""

    @abstractmethod
    async def get_by_course_and_name(self, course_id: UUID, name: str) -> Section | None:
        """Fetch section by course and section name."""

    @abstractmethod
    async def save(self, section: Section) -> Section:
        """Persist a section."""


class RoomRepository(ABC):
    @abstractmethod
    async def get_by_id(self, room_id: UUID) -> Room | None:
        """Fetch room by unique identifier."""

    @abstractmethod
    async def get_by_code(self, code: str) -> Room | None:
        """Fetch room by unique room code."""

    @abstractmethod
    async def save(self, room: Room) -> Room:
        """Persist a room."""


class TimetableUploadRepository(ABC):
    @abstractmethod
    async def get_by_id(self, upload_id: UUID) -> TimetableUpload | None:
        """Fetch timetable upload by unique identifier."""

    @abstractmethod
    async def list_by_term_id(self, term_id: UUID) -> list[TimetableUpload]:
        """List all timetable uploads for an academic term."""

    @abstractmethod
    async def save(self, upload: TimetableUpload) -> TimetableUpload:
        """Persist a timetable upload."""


class TimetableSlotRepository(ABC):
    @abstractmethod
    async def list_by_upload_id(self, upload_id: UUID) -> list[TimetableSlot]:
        """List all slots generated from an upload."""

    @abstractmethod
    async def list_by_faculty_id(self, faculty_id: UUID) -> list[TimetableSlot]:
        """List timetable slots assigned to a faculty member."""

    @abstractmethod
    async def save_all(self, slots: list[TimetableSlot]) -> list[TimetableSlot]:
        """Persist multiple timetable slots."""

    @abstractmethod
    async def delete_by_upload_id(self, upload_id: UUID) -> None:
        """Delete all slots associated with an upload."""


class UnitOfWork(ABC):
    departments: DepartmentRepository
    users: UserRepository
    faculty_profiles: FacultyProfileRepository
    academic_terms: AcademicTermRepository
    events: EventRepository
    circulars: CircularRepository
    notifications: NotificationRepository
    reminder_rules: ReminderRuleRepository
    push_subscriptions: PushSubscriptionRepository
    tasks: TaskRepository
    task_templates: TaskTemplateRepository
    audit_logs: AuditLogRepository
    refresh_tokens: RefreshTokenRepository
    timetable_uploads: TimetableUploadRepository
    timetable_slots: TimetableSlotRepository
    courses: CourseRepository
    sections: SectionRepository
    rooms: RoomRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        """Enter unit of work context."""

    @abstractmethod
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: object
    ) -> None:
        """Exit unit of work context, rolling back if exception occurred."""

    @abstractmethod
    async def commit(self) -> None:
        """Commit all transactional changes."""

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback transactional changes."""
