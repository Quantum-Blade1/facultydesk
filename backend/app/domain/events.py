from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent:
    event_id: UUID = field(default_factory=uuid4)
    occurred_at_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )


@dataclass(frozen=True)
class EventScheduled(DomainEvent):
    scheduled_event_id: UUID = field(default_factory=uuid4)
    title: str = ""
    start_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    end_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    attendee_ids: tuple[UUID, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class EventRescheduled(DomainEvent):
    scheduled_event_id: UUID = field(default_factory=uuid4)
    old_start_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    old_end_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    new_start_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    new_end_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )


@dataclass(frozen=True)
class EventCancelled(DomainEvent):
    scheduled_event_id: UUID = field(default_factory=uuid4)
    reason: str = ""


@dataclass(frozen=True)
class TaskCreated(DomainEvent):
    task_id: UUID = field(default_factory=uuid4)
    title: str = ""
    assignee_id: UUID = field(default_factory=uuid4)
    deadline_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )


@dataclass(frozen=True)
class TaskDeadlineChanged(DomainEvent):
    task_id: UUID = field(default_factory=uuid4)
    old_deadline_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    new_deadline_utc: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
