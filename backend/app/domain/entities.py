from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from typing import Any
from uuid import UUID, uuid4

from app.domain.errors import InvalidTransition, InvariantViolation
from app.domain.events import (
    DomainEvent,
    EventCancelled,
    EventRescheduled,
    TaskDeadlineChanged,
)
from app.domain.value_objects import (
    AttendeeResponse,
    CircularStatus,
    EventKind,
    EventSource,
    Initials,
    NotificationChannel,
    NotificationStatus,
    Role,
    TaskStatus,
    TimeSlot,
)


@dataclass
class Department:
    id: UUID = field(default_factory=uuid4)
    code: str = ""
    name: str = ""

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise InvariantViolation("Department code cannot be empty")
        if not self.name.strip():
            raise InvariantViolation("Department name cannot be empty")


@dataclass
class User:
    id: UUID = field(default_factory=uuid4)
    email: str = ""
    password_hash: str = ""
    role: Role = Role.FACULTY
    is_active: bool = True

    def __post_init__(self) -> None:
        if not self.email.strip() or "@" not in self.email:
            raise InvariantViolation(f"Invalid email: '{self.email}'")


@dataclass
class FacultyProfile:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    department_id: UUID = field(default_factory=uuid4)
    full_name: str = ""
    initials: Initials = field(default_factory=lambda: Initials("XX"))
    aliases: tuple[str, ...] = field(default_factory=tuple)
    email: str = ""
    phone: str | None = None

    def __post_init__(self) -> None:
        if not self.full_name.strip():
            raise InvariantViolation("Faculty full name cannot be empty")


@dataclass
class AcademicTerm:
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    start_date: date = field(default_factory=date.today)
    end_date: date = field(default_factory=date.today)
    timezone: str = "Asia/Kolkata"

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise InvariantViolation("Academic term name cannot be empty")
        if self.start_date >= self.end_date:
            msg = f"start_date ({self.start_date}) must be earlier than end_date ({self.end_date})"
            raise InvariantViolation(msg)


@dataclass
class Holiday:
    id: UUID = field(default_factory=uuid4)
    academic_term_id: UUID = field(default_factory=uuid4)
    date: date = field(default_factory=date.today)
    label: str = ""

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise InvariantViolation("Holiday label cannot be empty")


@dataclass
class Room:
    id: UUID = field(default_factory=uuid4)
    code: str = ""
    building: str = ""
    capacity: int = 60

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise InvariantViolation("Room code cannot be empty")
        if self.capacity <= 0:
            raise InvariantViolation("Room capacity must be positive")


@dataclass
class Course:
    id: UUID = field(default_factory=uuid4)
    department_id: UUID = field(default_factory=uuid4)
    code: str = ""
    name: str = ""
    credits: int = 3

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise InvariantViolation("Course code cannot be empty")
        if not self.name.strip():
            raise InvariantViolation("Course name cannot be empty")
        if self.credits <= 0:
            raise InvariantViolation("Course credits must be positive")


@dataclass
class Section:
    id: UUID = field(default_factory=uuid4)
    course_id: UUID = field(default_factory=uuid4)
    name: str = ""

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise InvariantViolation("Section name cannot be empty")


@dataclass
class TimetableUpload:
    id: UUID = field(default_factory=uuid4)
    department_id: UUID = field(default_factory=uuid4)
    academic_term_id: UUID = field(default_factory=uuid4)
    file_key: str = ""
    status: str = "PENDING"
    parse_report: dict[str, Any] = field(default_factory=dict)
    uploaded_at_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )


@dataclass
class TimetableSlot:
    id: UUID = field(default_factory=uuid4)
    timetable_upload_id: UUID = field(default_factory=uuid4)
    time_slot: TimeSlot = field(
        default_factory=lambda: TimeSlot(
            0,
            datetime.min.time(),
            datetime.max.time(),
        )
    )
    course_id: UUID = field(default_factory=uuid4)
    section_id: UUID = field(default_factory=uuid4)
    room_id: UUID = field(default_factory=uuid4)
    faculty_id: UUID = field(default_factory=uuid4)
    source_cell_reference: str = ""


@dataclass
class EventAttendee:
    id: UUID = field(default_factory=uuid4)
    event_id: UUID = field(default_factory=uuid4)
    faculty_id: UUID = field(default_factory=uuid4)
    response: AttendeeResponse = AttendeeResponse.INVITED


@dataclass
class Event:
    id: UUID = field(default_factory=uuid4)
    kind: EventKind = EventKind.CLASS
    title: str = ""
    start_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    end_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    location: str = ""
    source: EventSource = EventSource.MANUAL
    source_id: UUID | None = None
    attendees: list[EventAttendee] = field(default_factory=list)
    domain_events: list[DomainEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise InvariantViolation("Event title cannot be empty")
        if self.start_utc.tzinfo is None or self.end_utc.tzinfo is None:
            raise InvariantViolation("Event timestamps must be timezone-aware UTC")
        if self.start_utc >= self.end_utc:
            raise InvariantViolation(
                f"start_utc ({self.start_utc}) must precede end_utc ({self.end_utc})"
            )

    def reschedule(self, new_start_utc: datetime, new_end_utc: datetime) -> None:
        if new_start_utc.tzinfo is None or new_end_utc.tzinfo is None:
            raise InvariantViolation("Rescheduled timestamps must be timezone-aware UTC")
        if new_start_utc >= new_end_utc:
            raise InvariantViolation(
                f"new_start_utc ({new_start_utc}) must precede new_end_utc ({new_end_utc})"
            )
        old_start = self.start_utc
        old_end = self.end_utc
        self.start_utc = new_start_utc
        self.end_utc = new_end_utc
        self.domain_events.append(
            EventRescheduled(
                scheduled_event_id=self.id,
                old_start_utc=old_start,
                old_end_utc=old_end,
                new_start_utc=new_start_utc,
                new_end_utc=new_end_utc,
            )
        )

    def cancel(self, reason: str = "") -> None:
        self.domain_events.append(
            EventCancelled(
                scheduled_event_id=self.id,
                reason=reason,
            )
        )

    def add_attendee(
        self, faculty_id: UUID, response: AttendeeResponse = AttendeeResponse.INVITED
    ) -> None:
        for attendee in self.attendees:
            if attendee.faculty_id == faculty_id:
                return
        self.attendees.append(
            EventAttendee(
                event_id=self.id,
                faculty_id=faculty_id,
                response=response,
            )
        )


CIRCULAR_TRANSITIONS: dict[CircularStatus, set[CircularStatus]] = {
    CircularStatus.UPLOADED: {CircularStatus.PROCESSING},
    CircularStatus.PROCESSING: {
        CircularStatus.NEEDS_REVIEW,
        CircularStatus.CONFIRMED,
        CircularStatus.FAILED,
    },
    CircularStatus.NEEDS_REVIEW: {
        CircularStatus.CONFIRMED,
        CircularStatus.REJECTED,
    },
    CircularStatus.FAILED: {CircularStatus.PROCESSING},
    CircularStatus.CONFIRMED: set(),
    CircularStatus.REJECTED: set(),
}


@dataclass
class Circular:
    id: UUID = field(default_factory=uuid4)
    file_key: str = ""
    ocr_text: str = ""
    extracted_fields: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    status: CircularStatus = CircularStatus.UPLOADED
    failure_reason: str | None = None

    def _transition(self, target: CircularStatus) -> None:
        allowed = CIRCULAR_TRANSITIONS.get(self.status, set())
        if target not in allowed:
            raise InvalidTransition(self.status.value, target.value, "Circular")
        self.status = target

    def start_processing(self) -> None:
        self._transition(CircularStatus.PROCESSING)
        self.failure_reason = None

    def mark_needs_review(self, extracted_fields: dict[str, Any], confidence: float) -> None:
        self._transition(CircularStatus.NEEDS_REVIEW)
        self.extracted_fields = extracted_fields
        self.confidence = confidence

    def confirm(self, extracted_fields: dict[str, Any] | None = None) -> None:
        self._transition(CircularStatus.CONFIRMED)
        if extracted_fields is not None:
            self.extracted_fields = extracted_fields

    def reject(self, reason: str = "") -> None:
        self._transition(CircularStatus.REJECTED)
        self.failure_reason = reason

    def fail(self, reason: str) -> None:
        self._transition(CircularStatus.FAILED)
        self.failure_reason = reason


NOTIFICATION_TRANSITIONS: dict[NotificationStatus, set[NotificationStatus]] = {
    NotificationStatus.PENDING: {
        NotificationStatus.SENDING,
        NotificationStatus.CANCELLED,
    },
    NotificationStatus.SENDING: {
        NotificationStatus.SENT,
        NotificationStatus.FAILED,
    },
    NotificationStatus.FAILED: {NotificationStatus.PENDING},
    NotificationStatus.SENT: set(),
    NotificationStatus.CANCELLED: set(),
}


@dataclass
class ScheduledNotification:
    id: UUID = field(default_factory=uuid4)
    target_id: UUID = field(default_factory=uuid4)
    target_kind: str = "EVENT"
    user_id: UUID = field(default_factory=uuid4)
    channel: NotificationChannel = NotificationChannel.EMAIL
    fire_at_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    idempotency_key: str = ""
    attempts: int = 0
    max_attempts: int = 3
    last_error: str | None = None
    status: NotificationStatus = NotificationStatus.PENDING

    def _transition(self, target: NotificationStatus) -> None:
        allowed = NOTIFICATION_TRANSITIONS.get(self.status, set())
        if target not in allowed:
            raise InvalidTransition(self.status.value, target.value, "ScheduledNotification")
        self.status = target

    def mark_sending(self) -> None:
        self._transition(NotificationStatus.SENDING)
        self.attempts += 1

    def mark_sent(self) -> None:
        self._transition(NotificationStatus.SENT)
        self.last_error = None

    def mark_failed(self, error: str) -> None:
        self._transition(NotificationStatus.FAILED)
        self.last_error = error

    def retry(self) -> None:
        if self.attempts >= self.max_attempts:
            raise InvariantViolation(
                f"Cannot retry notification: reached max attempts ({self.max_attempts})"
            )
        self._transition(NotificationStatus.PENDING)

    def cancel(self) -> None:
        self._transition(NotificationStatus.CANCELLED)


@dataclass
class ReminderRule:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    event_kind: EventKind = EventKind.CLASS
    offsets_minutes: tuple[int, ...] = (15, 60)
    channels: tuple[NotificationChannel, ...] = (NotificationChannel.EMAIL,)

    def __post_init__(self) -> None:
        for offset in self.offsets_minutes:
            if offset < 0:
                raise InvariantViolation(f"Offset minutes cannot be negative: {offset}")


@dataclass
class PushSubscription:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID = field(default_factory=uuid4)
    endpoint: str = ""
    p256dh: str = ""
    auth: str = ""

    def __post_init__(self) -> None:
        if not self.endpoint.strip():
            raise InvariantViolation("Subscription endpoint cannot be empty")
        if not self.p256dh.strip():
            raise InvariantViolation("Subscription p256dh key cannot be empty")
        if not self.auth.strip():
            raise InvariantViolation("Subscription auth secret cannot be empty")


@dataclass
class Task:
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    description: str = ""
    deadline_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    importance: int = 3
    status: TaskStatus = TaskStatus.TODO
    assignee_id: UUID = field(default_factory=uuid4)
    assigner_id: UUID = field(default_factory=uuid4)
    domain_events: list[DomainEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise InvariantViolation("Task title cannot be empty")
        if not (1 <= self.importance <= 5):
            raise InvariantViolation(
                f"Task importance must be between 1 and 5, got: {self.importance}"
            )
        if self.deadline_utc.tzinfo is None:
            raise InvariantViolation("Task deadline must be timezone-aware UTC")

    def update_deadline(self, new_deadline_utc: datetime) -> None:
        if new_deadline_utc.tzinfo is None:
            raise InvariantViolation("Task deadline must be timezone-aware UTC")
        old_deadline = self.deadline_utc
        self.deadline_utc = new_deadline_utc
        self.domain_events.append(
            TaskDeadlineChanged(
                task_id=self.id,
                old_deadline_utc=old_deadline,
                new_deadline_utc=new_deadline_utc,
            )
        )

    def change_status(self, new_status: TaskStatus) -> None:
        self.status = new_status


@dataclass
class AuditLog:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID | None = None
    action: str = ""
    resource_type: str = ""
    resource_id: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    def __post_init__(self) -> None:
        if not self.action.strip():
            raise InvariantViolation("AuditLog action cannot be empty")
        if not self.resource_type.strip():
            raise InvariantViolation("AuditLog resource_type cannot be empty")
