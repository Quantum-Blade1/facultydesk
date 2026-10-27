"""reminder_rules_quiet_hours_and_delivery

Revision ID: 1c007141bd6c
Revises: 9bad995bed3e
Create Date: 2026-10-27 19:36:36.043661

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = '1c007141bd6c'
down_revision: str | Sequence[str] | None = '9bad995bed3e'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("quiet_hours_start", sa.Time(), nullable=True))
    op.add_column("users", sa.Column("quiet_hours_end", sa.Time(), nullable=True))
    op.add_column(
        "scheduled_notifications",
        sa.Column("delivered_at_utc", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_unique_constraint(
        "uq_reminder_rules_user_event_kind",
        "reminder_rules",
        ["user_id", "event_kind"],
    )
    op.create_unique_constraint(
        "uq_push_subscriptions_user_endpoint",
        "push_subscriptions",
        ["user_id", "endpoint"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_push_subscriptions_user_endpoint",
        "push_subscriptions",
        type_="unique",
    )
    op.drop_constraint(
        "uq_reminder_rules_user_event_kind",
        "reminder_rules",
        type_="unique",
    )
    op.drop_column("scheduled_notifications", "delivered_at_utc")
    op.drop_column("users", "quiet_hours_end")
    op.drop_column("users", "quiet_hours_start")
