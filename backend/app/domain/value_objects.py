import re
from dataclasses import dataclass
from datetime import time
from enum import StrEnum

from app.domain.errors import InvariantViolation

INITIALS_REGEX = re.compile(r"\A[A-Z]{2,5}\Z")


class Role(StrEnum):
    ADMIN = "ADMIN"
    HOD = "HOD"
    FACULTY = "FACULTY"


@dataclass(frozen=True)
class Initials:
    value: str

    def __post_init__(self) -> None:
        if not INITIALS_REGEX.match(self.value):
            raise InvariantViolation(
                f"Initials must consist of 2 to 5 uppercase ASCII letters, got: '{self.value}'"
            )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class TimeSlot:
    weekday: int
    start_time: time
    end_time: time

    def __post_init__(self) -> None:
        if not (0 <= self.weekday <= 6):
            raise InvariantViolation(
                f"Weekday must be in range 0 (Monday) to 6 (Sunday), got: {self.weekday}"
            )
        if self.start_time >= self.end_time:
            msg = f"start_time ({self.start_time}) must be earlier than end_time ({self.end_time})"
            raise InvariantViolation(msg)

    def overlaps(self, other: "TimeSlot") -> bool:
        if self.weekday != other.weekday:
            return False
        return max(self.start_time, other.start_time) < min(self.end_time, other.end_time)


@dataclass(frozen=True)
class QuietHours:
    start_time: time
    end_time: time

    @property
    def crosses_midnight(self) -> bool:
        return self.start_time > self.end_time

    def covers(self, t: time) -> bool:
        if self.start_time == self.end_time:
            return False
        if not self.crosses_midnight:
            return self.start_time <= t < self.end_time
        return t >= self.start_time or t < self.end_time


class EventKind(StrEnum):
    CLASS = "CLASS"
    MEETING = "MEETING"
    DEADLINE = "DEADLINE"
    CUSTOM = "CUSTOM"


class EventSource(StrEnum):
    TIMETABLE = "TIMETABLE"
    CIRCULAR = "CIRCULAR"
    MANUAL = "MANUAL"
    TASK = "TASK"


class AttendeeResponse(StrEnum):
    INVITED = "INVITED"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    TENTATIVE = "TENTATIVE"


class CircularStatus(StrEnum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


class NotificationChannel(StrEnum):
    PUSH = "PUSH"
    EMAIL = "EMAIL"


class NotificationStatus(StrEnum):
    PENDING = "PENDING"
    SENDING = "SENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class TaskStatus(StrEnum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class TimetableUploadStatus(StrEnum):
    UPLOADED = "UPLOADED"
    PARSING = "PARSING"
    PREVIEW_READY = "PREVIEW_READY"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"

