from datetime import UTC, date, datetime, timedelta

from hypothesis import given
from hypothesis import strategies as st

from app.application.tasks.maths import (
    compute_completion_rate,
    compute_lead_alert_times,
    compute_overdue_alert_times,
    compute_priority_score,
)


def test_priority_worked_example_table() -> None:
    now_utc = datetime(2026, 10, 27, 10, 0, tzinfo=UTC)

    # T1: Overdue by 2 days, Importance 5
    p1 = compute_priority_score(
        importance=5,
        deadline_utc=datetime(2026, 10, 25, 10, 0, tzinfo=UTC),
        now_utc=now_utc,
    )
    assert p1 == round(1.0 + (2.0 / 7.0), 4)
    assert p1 == 1.2857

    # T2: Due in 6h, Importance 5
    p2 = compute_priority_score(
        importance=5,
        deadline_utc=datetime(2026, 10, 27, 16, 0, tzinfo=UTC),
        now_utc=now_utc,
    )
    assert p2 == 0.9295

    # T3: Due in 12h, Importance 3
    p3 = compute_priority_score(
        importance=3,
        deadline_utc=datetime(2026, 10, 27, 22, 0, tzinfo=UTC),
        now_utc=now_utc,
    )
    assert p3 == 0.6673

    # T4: Due in 72h, Importance 4
    p4 = compute_priority_score(
        importance=4,
        deadline_utc=datetime(2026, 10, 30, 10, 0, tzinfo=UTC),
        now_utc=now_utc,
    )
    assert p4 == 0.4339

    # T5: Due in 120h, Importance 2
    p5 = compute_priority_score(
        importance=2,
        deadline_utc=datetime(2026, 11, 1, 10, 0, tzinfo=UTC),
        now_utc=now_utc,
    )
    assert p5 == 0.1493

    assert p1 > p2 > p3 > p4 > p5


@given(
    importance=st.integers(min_value=1, max_value=5),
    hours_remaining=st.floats(min_value=0.01, max_value=5000.0, allow_nan=False),
)
def test_priority_bounds_property_active(importance: int, hours_remaining: float) -> None:
    now_utc = datetime(2026, 10, 27, 10, 0, tzinfo=UTC)
    deadline = now_utc + timedelta(hours=hours_remaining)
    p = compute_priority_score(importance, deadline, now_utc)
    assert 0.0 <= p <= 1.0


@given(
    importance=st.integers(min_value=1, max_value=5),
    days_overdue=st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
)
def test_priority_bounds_property_overdue(importance: int, days_overdue: float) -> None:
    now_utc = datetime(2026, 10, 27, 10, 0, tzinfo=UTC)
    deadline = now_utc - timedelta(days=days_overdue)
    p = compute_priority_score(importance, deadline, now_utc)
    assert 1.0 <= p <= 2.0


def test_priority_monotonicity_hours() -> None:
    now_utc = datetime(2026, 10, 27, 10, 0, tzinfo=UTC)
    p_close = compute_priority_score(4, now_utc + timedelta(hours=4), now_utc)
    p_far = compute_priority_score(4, now_utc + timedelta(hours=24), now_utc)
    assert p_close > p_far


def test_priority_monotonicity_importance() -> None:
    now_utc = datetime(2026, 10, 27, 10, 0, tzinfo=UTC)
    p_low = compute_priority_score(2, now_utc + timedelta(hours=10), now_utc)
    p_high = compute_priority_score(5, now_utc + timedelta(hours=10), now_utc)
    assert p_high > p_low


def test_completed_task_priority() -> None:
    now_utc = datetime(2026, 10, 27, 10, 0, tzinfo=UTC)
    p = compute_priority_score(5, now_utc + timedelta(hours=1), now_utc, is_completed=True)
    assert p == -1.0


def test_lead_alert_times() -> None:
    created = datetime(2026, 10, 25, 10, 0, tzinfo=UTC)
    deadline = datetime(2026, 10, 29, 10, 0, tzinfo=UTC)  # 96 hours later
    alerts = compute_lead_alert_times(deadline, created)
    assert len(alerts) == 3
    assert alerts[0] == deadline - timedelta(hours=72)
    assert alerts[1] == deadline - timedelta(hours=24)
    assert alerts[2] == deadline - timedelta(hours=2)

    created_late = deadline - timedelta(hours=10)
    alerts_late = compute_lead_alert_times(deadline, created_late)
    assert len(alerts_late) == 1
    assert alerts_late[0] == deadline - timedelta(hours=2)


def test_overdue_alert_times() -> None:
    deadline = datetime(2026, 10, 25, 4, 30, tzinfo=UTC)  # 10:00 AM IST
    until = date(2026, 10, 27)
    alerts = compute_overdue_alert_times(deadline, until)
    assert len(alerts) == 2
    assert alerts[0] == datetime(2026, 10, 26, 3, 30, tzinfo=UTC)
    assert alerts[1] == datetime(2026, 10, 27, 3, 30, tzinfo=UTC)


def test_completion_rate() -> None:
    assert compute_completion_rate(0, 0) == 100.0
    assert compute_completion_rate(10, 5) == 50.0
    assert compute_completion_rate(3, 1) == 33.33
