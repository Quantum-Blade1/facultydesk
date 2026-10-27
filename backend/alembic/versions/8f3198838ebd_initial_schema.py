"""initial_schema

Revision ID: 8f3198838ebd
Revises:
Create Date: 2026-10-27 08:01:17.929130

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "8f3198838ebd"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "academic_terms",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False),
        sa.CheckConstraint("end_date > start_date", name="ck_academic_terms_dates"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "circulars",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("file_key", sa.String(length=255), nullable=False),
        sa.Column("ocr_text", sa.Text(), nullable=False),
        sa.Column("extracted_fields", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column("created_at_utc", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_circulars_status"), "circulars", ["status"], unique=False)
    op.create_table(
        "departments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at_utc", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_departments_code"), "departments", ["code"], unique=True)
    op.create_table(
        "events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("start_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("location", sa.String(length=255), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("source_id", sa.Uuid(), nullable=True),
        sa.Column("created_at_utc", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("end_utc > start_utc", name="ck_events_interval"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_events_start_end", "events", ["start_utc", "end_utc"], unique=False)
    op.create_index(op.f("ix_events_start_utc"), "events", ["start_utc"], unique=False)
    op.create_table(
        "rooms",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("building", sa.String(length=128), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rooms_code"), "rooms", ["code"], unique=True)
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at_utc", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("resource_type", sa.String(length=64), nullable=False),
        sa.Column("resource_id", sa.String(length=128), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("timestamp_utc", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_audit_logs_resource", "audit_logs", ["resource_type", "resource_id"], unique=False
    )
    op.create_index(
        op.f("ix_audit_logs_timestamp_utc"), "audit_logs", ["timestamp_utc"], unique=False
    )
    op.create_index(op.f("ix_audit_logs_user_id"), "audit_logs", ["user_id"], unique=False)
    op.create_table(
        "courses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("department_id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("credits", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("department_id", "code", name="uq_courses_department_code"),
    )
    op.create_index(op.f("ix_courses_department_id"), "courses", ["department_id"], unique=False)
    op.create_table(
        "faculty_profiles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("department_id", sa.Uuid(), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("initials", sa.String(length=10), nullable=False),
        sa.Column("aliases", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("department_id", "initials", name="uq_faculty_department_initials"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(
        op.f("ix_faculty_profiles_department_id"),
        "faculty_profiles",
        ["department_id"],
        unique=False,
    )
    op.create_table(
        "holidays",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("academic_term_id", sa.Uuid(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["academic_term_id"], ["academic_terms.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_holidays_academic_term_id"), "holidays", ["academic_term_id"], unique=False
    )
    op.create_table(
        "push_subscriptions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("endpoint", sa.Text(), nullable=False),
        sa.Column("p256dh", sa.Text(), nullable=False),
        sa.Column("auth", sa.Text(), nullable=False),
        sa.Column("created_at_utc", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_push_subscriptions_user_id"), "push_subscriptions", ["user_id"], unique=False
    )
    op.create_table(
        "reminder_rules",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("event_kind", sa.String(length=32), nullable=False),
        sa.Column("offsets_minutes", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("channels", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reminder_rules_user_id"), "reminder_rules", ["user_id"], unique=False)
    op.create_table(
        "scheduled_notifications",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("target_id", sa.Uuid(), nullable=False),
        sa.Column("target_kind", sa.String(length=32), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("fire_at_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("idempotency_key", sa.String(length=255), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("max_attempts", sa.Integer(), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_notifications_status_fire_at",
        "scheduled_notifications",
        ["status", "fire_at_utc"],
        unique=False,
    )
    op.create_index(
        op.f("ix_scheduled_notifications_fire_at_utc"),
        "scheduled_notifications",
        ["fire_at_utc"],
        unique=False,
    )
    op.create_index(
        op.f("ix_scheduled_notifications_idempotency_key"),
        "scheduled_notifications",
        ["idempotency_key"],
        unique=True,
    )
    op.create_index(
        op.f("ix_scheduled_notifications_user_id"),
        "scheduled_notifications",
        ["user_id"],
        unique=False,
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("deadline_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("importance", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("assignee_id", sa.Uuid(), nullable=False),
        sa.Column("assigner_id", sa.Uuid(), nullable=False),
        sa.Column("created_at_utc", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("importance >= 1 AND importance <= 5", name="ck_tasks_importance"),
        sa.ForeignKeyConstraint(["assignee_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["assigner_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_tasks_assignee_deadline", "tasks", ["assignee_id", "deadline_utc"], unique=False
    )
    op.create_index(op.f("ix_tasks_assignee_id"), "tasks", ["assignee_id"], unique=False)
    op.create_index(op.f("ix_tasks_deadline_utc"), "tasks", ["deadline_utc"], unique=False)
    op.create_table(
        "timetable_uploads",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("department_id", sa.Uuid(), nullable=False),
        sa.Column("academic_term_id", sa.Uuid(), nullable=False),
        sa.Column("file_key", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("parse_report", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("uploaded_at_utc", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["academic_term_id"], ["academic_terms.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["department_id"], ["departments.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_timetable_uploads_academic_term_id"),
        "timetable_uploads",
        ["academic_term_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_timetable_uploads_department_id"),
        "timetable_uploads",
        ["department_id"],
        unique=False,
    )
    op.create_table(
        "event_attendees",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("event_id", sa.Uuid(), nullable=False),
        sa.Column("faculty_id", sa.Uuid(), nullable=False),
        sa.Column("response", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["faculty_id"], ["faculty_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id", "faculty_id", name="uq_event_attendee"),
    )
    op.create_index(
        op.f("ix_event_attendees_event_id"), "event_attendees", ["event_id"], unique=False
    )
    op.create_index(
        "ix_event_attendees_faculty_event",
        "event_attendees",
        ["faculty_id", "event_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_event_attendees_faculty_id"), "event_attendees", ["faculty_id"], unique=False
    )
    op.create_table(
        "sections",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("course_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sections_course_id"), "sections", ["course_id"], unique=False)
    op.create_table(
        "timetable_slots",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("timetable_upload_id", sa.Uuid(), nullable=False),
        sa.Column("weekday", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("course_id", sa.Uuid(), nullable=False),
        sa.Column("section_id", sa.Uuid(), nullable=False),
        sa.Column("room_id", sa.Uuid(), nullable=False),
        sa.Column("faculty_id", sa.Uuid(), nullable=False),
        sa.Column("source_cell_reference", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["faculty_id"], ["faculty_profiles.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["section_id"], ["sections.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["timetable_upload_id"], ["timetable_uploads.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_timetable_slots_faculty_id"), "timetable_slots", ["faculty_id"], unique=False
    )
    op.create_index(
        op.f("ix_timetable_slots_timetable_upload_id"),
        "timetable_slots",
        ["timetable_upload_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_timetable_slots_timetable_upload_id"), table_name="timetable_slots")
    op.drop_index(op.f("ix_timetable_slots_faculty_id"), table_name="timetable_slots")
    op.drop_table("timetable_slots")
    op.drop_index(op.f("ix_sections_course_id"), table_name="sections")
    op.drop_table("sections")
    op.drop_index(op.f("ix_event_attendees_faculty_id"), table_name="event_attendees")
    op.drop_index("ix_event_attendees_faculty_event", table_name="event_attendees")
    op.drop_index(op.f("ix_event_attendees_event_id"), table_name="event_attendees")
    op.drop_table("event_attendees")
    op.drop_index(op.f("ix_timetable_uploads_department_id"), table_name="timetable_uploads")
    op.drop_index(op.f("ix_timetable_uploads_academic_term_id"), table_name="timetable_uploads")
    op.drop_table("timetable_uploads")
    op.drop_index(op.f("ix_tasks_deadline_utc"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_assignee_id"), table_name="tasks")
    op.drop_index("ix_tasks_assignee_deadline", table_name="tasks")
    op.drop_table("tasks")
    op.drop_index(op.f("ix_scheduled_notifications_user_id"), table_name="scheduled_notifications")
    op.drop_index(
        op.f("ix_scheduled_notifications_idempotency_key"), table_name="scheduled_notifications"
    )
    op.drop_index(
        op.f("ix_scheduled_notifications_fire_at_utc"), table_name="scheduled_notifications"
    )
    op.drop_index("ix_notifications_status_fire_at", table_name="scheduled_notifications")
    op.drop_table("scheduled_notifications")
    op.drop_index(op.f("ix_reminder_rules_user_id"), table_name="reminder_rules")
    op.drop_table("reminder_rules")
    op.drop_index(op.f("ix_push_subscriptions_user_id"), table_name="push_subscriptions")
    op.drop_table("push_subscriptions")
    op.drop_index(op.f("ix_holidays_academic_term_id"), table_name="holidays")
    op.drop_table("holidays")
    op.drop_index(op.f("ix_faculty_profiles_department_id"), table_name="faculty_profiles")
    op.drop_table("faculty_profiles")
    op.drop_index(op.f("ix_courses_department_id"), table_name="courses")
    op.drop_table("courses")
    op.drop_index(op.f("ix_audit_logs_user_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_timestamp_utc"), table_name="audit_logs")
    op.drop_index("ix_audit_logs_resource", table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_rooms_code"), table_name="rooms")
    op.drop_table("rooms")
    op.drop_index(op.f("ix_events_start_utc"), table_name="events")
    op.drop_index("ix_events_start_end", table_name="events")
    op.drop_table("events")
    op.drop_index(op.f("ix_departments_code"), table_name="departments")
    op.drop_table("departments")
    op.drop_index(op.f("ix_circulars_status"), table_name="circulars")
    op.drop_table("circulars")
    op.drop_table("academic_terms")
