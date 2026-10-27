import uuid
from datetime import UTC, date, datetime, time
from typing import Any

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class DepartmentModel(Base):
    __tablename__ = "departments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    faculty_profiles: Mapped[list["FacultyProfileModel"]] = relationship(
        back_populates="department", cascade="all, delete-orphan"
    )
    courses: Mapped[list["CourseModel"]] = relationship(
        back_populates="department", cascade="all, delete-orphan"
    )


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="FACULTY")
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    profile: Mapped["FacultyProfileModel | None"] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class FacultyProfileModel(Base):
    __tablename__ = "faculty_profiles"
    __table_args__ = (
        UniqueConstraint("department_id", "initials", name="uq_faculty_department_initials"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    initials: Mapped[str] = mapped_column(String(10), nullable=False)
    aliases: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)

    user: Mapped[UserModel] = relationship(back_populates="profile")
    department: Mapped[DepartmentModel] = relationship(back_populates="faculty_profiles")


class AcademicTermModel(Base):
    __tablename__ = "academic_terms"
    __table_args__ = (
        CheckConstraint("end_date > start_date", name="ck_academic_terms_dates"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="Asia/Kolkata")

    holidays: Mapped[list["HolidayModel"]] = relationship(
        back_populates="academic_term", cascade="all, delete-orphan"
    )


class HolidayModel(Base):
    __tablename__ = "holidays"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("academic_terms.id", ondelete="CASCADE"), nullable=False, index=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=False)

    academic_term: Mapped[AcademicTermModel] = relationship(back_populates="holidays")


class RoomModel(Base):
    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    building: Mapped[str] = mapped_column(String(128), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=60)


class CourseModel(Base):
    __tablename__ = "courses"
    __table_args__ = (
        UniqueConstraint("department_id", "code", name="uq_courses_department_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    credits: Mapped[int] = mapped_column(Integer, nullable=False, default=3)

    department: Mapped[DepartmentModel] = relationship(back_populates="courses")
    sections: Mapped[list["SectionModel"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )


class SectionModel(Base):
    __tablename__ = "sections"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(32), nullable=False)

    course: Mapped[CourseModel] = relationship(back_populates="sections")


class TimetableUploadModel(Base):
    __tablename__ = "timetable_uploads"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    department_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    academic_term_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("academic_terms.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    file_key: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING")
    parse_report: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    uploaded_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )


class TimetableSlotModel(Base):
    __tablename__ = "timetable_slots"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    timetable_upload_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("timetable_uploads.id", ondelete="CASCADE"), nullable=False, index=True
    )
    weekday: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False
    )
    section_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("sections.id", ondelete="RESTRICT"), nullable=False
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("rooms.id", ondelete="RESTRICT"), nullable=False
    )
    faculty_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("faculty_profiles.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    source_cell_reference: Mapped[str] = mapped_column(String(64), nullable=False)


class EventModel(Base):
    __tablename__ = "events"
    __table_args__ = (
        CheckConstraint("end_utc > start_utc", name="ck_events_interval"),
        Index("ix_events_start_end", "start_utc", "end_utc"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    start_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    end_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    source_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    created_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    attendees: Mapped[list["EventAttendeeModel"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )


class EventAttendeeModel(Base):
    __tablename__ = "event_attendees"
    __table_args__ = (
        UniqueConstraint("event_id", "faculty_id", name="uq_event_attendee"),
        Index("ix_event_attendees_faculty_event", "faculty_id", "event_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    faculty_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("faculty_profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    response: Mapped[str] = mapped_column(String(32), nullable=False, default="INVITED")

    event: Mapped[EventModel] = relationship(back_populates="attendees")


class CircularModel(Base):
    __tablename__ = "circulars"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    file_key: Mapped[str] = mapped_column(String(255), nullable=False)
    ocr_text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    extracted_fields: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="UPLOADED", index=True)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )


class ScheduledNotificationModel(Base):
    __tablename__ = "scheduled_notifications"
    __table_args__ = (
        Index("ix_notifications_status_fire_at", "status", "fire_at_utc"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    target_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    target_kind: Mapped[str] = mapped_column(String(32), nullable=False, default="EVENT")
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    channel: Mapped[str] = mapped_column(String(32), nullable=False)
    fire_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    idempotency_key: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING")


class ReminderRuleModel(Base):
    __tablename__ = "reminder_rules"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    offsets_minutes: Mapped[list[int]] = mapped_column(JSONB, nullable=False)
    channels: Mapped[list[str]] = mapped_column(JSONB, nullable=False)


class PushSubscriptionModel(Base):
    __tablename__ = "push_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    endpoint: Mapped[str] = mapped_column(Text, nullable=False)
    p256dh: Mapped[str] = mapped_column(Text, nullable=False)
    auth: Mapped[str] = mapped_column(Text, nullable=False)
    created_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )


class TaskModel(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("importance >= 1 AND importance <= 5", name="ck_tasks_importance"),
        Index("ix_tasks_assignee_deadline", "assignee_id", "deadline_utc"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    deadline_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    importance: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="TODO")
    assignee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    assigner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    created_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )


class AuditLogModel(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_audit_logs_resource", "resource_type", "resource_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(64), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(128), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    timestamp_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        index=True,
    )
