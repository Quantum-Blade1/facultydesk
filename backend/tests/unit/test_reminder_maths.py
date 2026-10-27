from datetime import UTC, datetime, time
from uuid import uuid4
from zoneinfo import ZoneInfo

from hypothesis import given
from hypothesis import strategies as st

from app.application.reminders.maths import (
    adjust_for_quiet_hours,
    compute_backoff_delay,
    compute_fire_time,
    compute_idempotency_key,
)
from app.domain.value_objects import NotificationChannel, QuietHours


def test_fire_time_computation() -> None:
    start = datetime(2026, 10, 28, 10, 0, tzinfo=UTC)
    fire_15 = compute_fire_time(start, 15)
    assert fire_15 == datetime(2026, 10, 28, 9, 45, tzinfo=UTC)

    fire_1440 = compute_fire_time(start, 1440)
    assert fire_1440 == datetime(2026, 10, 27, 10, 0, tzinfo=UTC)


def test_idempotency_key_deterministic() -> None:
    target_id = uuid4()
    user_id = uuid4()
    key1 = compute_idempotency_key(target_id, user_id, 15, NotificationChannel.EMAIL)
    key2 = compute_idempotency_key(target_id, user_id, 15, NotificationChannel.EMAIL)
    assert key1 == key2
    assert len(key1) == 64

    key_push = compute_idempotency_key(target_id, user_id, 15, NotificationChannel.PUSH)
    assert key1 != key_push

    key_diff_offset = compute_idempotency_key(target_id, user_id, 60, NotificationChannel.EMAIL)
    assert key1 != key_diff_offset


@given(attempt=st.integers(min_value=0, max_value=100))
def test_backoff_bounds(attempt: int) -> None:
    delay = compute_backoff_delay(attempt, base_seconds=30.0, cap_seconds=1800.0)
    assert 0.0 <= delay <= 1800.0


def test_quiet_hours_table() -> None:
    tz = ZoneInfo("Asia/Kolkata")
    overnight = QuietHours(time(22, 0), time(7, 0))
    same_day = QuietHours(time(13, 0), time(14, 0))
    disabled = QuietHours(time(7, 0), time(7, 0))

    fire_dt = datetime(2026, 10, 28, 15, 0, tzinfo=tz).astimezone(UTC)
    event_dt = datetime(2026, 10, 28, 16, 0, tzinfo=tz).astimezone(UTC)
    res = adjust_for_quiet_hours(fire_dt, event_dt, overnight)
    assert res == fire_dt

    fire_dt = datetime(2026, 10, 28, 23, 30, tzinfo=tz).astimezone(UTC)
    event_dt = datetime(2026, 10, 29, 10, 0, tzinfo=tz).astimezone(UTC)
    expected_shifted = datetime(2026, 10, 29, 7, 0, tzinfo=tz).astimezone(UTC)
    res = adjust_for_quiet_hours(fire_dt, event_dt, overnight)
    assert res == expected_shifted

    fire_dt = datetime(2026, 10, 29, 2, 0, tzinfo=tz).astimezone(UTC)
    event_dt = datetime(2026, 10, 29, 10, 0, tzinfo=tz).astimezone(UTC)
    expected_shifted = datetime(2026, 10, 29, 7, 0, tzinfo=tz).astimezone(UTC)
    res = adjust_for_quiet_hours(fire_dt, event_dt, overnight)
    assert res == expected_shifted

    fire_dt = datetime(2026, 10, 29, 6, 30, tzinfo=tz).astimezone(UTC)
    event_dt = datetime(2026, 10, 29, 6, 45, tzinfo=tz).astimezone(UTC)
    res = adjust_for_quiet_hours(fire_dt, event_dt, overnight)
    assert res == fire_dt

    fire_dt = datetime(2026, 10, 29, 13, 15, tzinfo=tz).astimezone(UTC)
    event_dt = datetime(2026, 10, 29, 15, 0, tzinfo=tz).astimezone(UTC)
    expected_shifted = datetime(2026, 10, 29, 14, 0, tzinfo=tz).astimezone(UTC)
    res = adjust_for_quiet_hours(fire_dt, event_dt, same_day)
    assert res == expected_shifted

    fire_dt = datetime(2026, 10, 29, 13, 15, tzinfo=tz).astimezone(UTC)
    event_dt = datetime(2026, 10, 29, 15, 0, tzinfo=tz).astimezone(UTC)
    res = adjust_for_quiet_hours(fire_dt, event_dt, disabled)
    assert res == fire_dt
