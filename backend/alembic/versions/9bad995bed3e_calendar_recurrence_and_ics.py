"""calendar_recurrence_and_ics

Revision ID: 9bad995bed3e
Revises: 8434d6a0dd0a
Create Date: 2026-10-27 13:22:53.653984

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9bad995bed3e'
down_revision: str | Sequence[str] | None = '8434d6a0dd0a'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('events', sa.Column('recurrence_date', sa.Date(), nullable=True))
    op.create_index(op.f('ix_events_recurrence_date'), 'events', ['recurrence_date'], unique=False)
    op.create_unique_constraint('uq_events_source_recurrence', 'events', ['source_id', 'recurrence_date'])

    op.add_column('faculty_profiles', sa.Column('ics_token', sa.String(length=64), nullable=True))
    op.execute("UPDATE faculty_profiles SET ics_token = md5(random()::text || clock_timestamp()::text) || md5(id::text) WHERE ics_token IS NULL")
    op.alter_column('faculty_profiles', 'ics_token', nullable=False)
    op.create_index(op.f('ix_faculty_profiles_ics_token'), 'faculty_profiles', ['ics_token'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_faculty_profiles_ics_token'), table_name='faculty_profiles')
    op.drop_column('faculty_profiles', 'ics_token')

    op.drop_constraint('uq_events_source_recurrence', 'events', type_='unique')
    op.drop_index(op.f('ix_events_recurrence_date'), table_name='events')
    op.drop_column('events', 'recurrence_date')

