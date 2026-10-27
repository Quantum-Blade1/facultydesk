"""task_categories_parent_assignment_and_templates

Revision ID: 005ce1a0ebb1
Revises: 1c007141bd6c
Create Date: 2026-10-27 23:54:35.460882

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '005ce1a0ebb1'
down_revision: str | Sequence[str] | None = '1c007141bd6c'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "category",
            sa.String(64),
            nullable=False,
            server_default="Academic documentation",
        ),
    )
    op.add_column(
        "tasks",
        sa.Column("parent_assignment_id", sa.Uuid(), nullable=True),
    )
    op.create_index(
        "ix_tasks_parent_assignment",
        "tasks",
        ["parent_assignment_id"],
    )
    op.add_column(
        "tasks",
        sa.Column("recurrence", sa.String(32), nullable=True),
    )

    op.create_table(
        "task_templates",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "department_id",
            sa.Uuid(),
            sa.ForeignKey("departments.id", ondelete="CASCADE"),
            nullable=True,
            index=True,
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column(
            "category",
            sa.String(64),
            nullable=False,
            server_default="Academic documentation",
        ),
        sa.Column("default_lead_days", sa.Integer(), nullable=False, server_default="7"),
        sa.Column("default_importance", sa.Integer(), nullable=False, server_default="3"),
        sa.Column(
            "created_at_utc",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("task_templates")
    op.drop_index("ix_tasks_parent_assignment", table_name="tasks")
    op.drop_column("tasks", "recurrence")
    op.drop_column("tasks", "parent_assignment_id")
    op.drop_column("tasks", "category")
