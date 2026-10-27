from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.core.clock import Clock, FrozenClock, SystemClock


def test_frozen_clock_rejects_naive_datetime() -> None:
    naive_dt = datetime(2026, 10, 27, 10, 0, 0)
    with pytest.raises(ValueError, match="timezone-aware"):
        FrozenClock(naive_dt)


@given(
    year=st.integers(min_value=2000, max_value=2050),
    month=st.integers(min_value=1, max_value=12),
    day=st.integers(min_value=1, max_value=28),
    hour=st.integers(min_value=0, max_value=23),
    minute=st.integers(min_value=0, max_value=59),
    second=st.integers(min_value=0, max_value=59),
)
def test_clock_always_returns_utc_property(
    year: int, month: int, day: int, hour: int, minute: int, second: int
) -> None:
    aware_dt = datetime(year, month, day, hour, minute, second, tzinfo=ZoneInfo("Asia/Kolkata"))
    clock: Clock = FrozenClock(aware_dt)
    current = clock.now()
    assert current.tzinfo == UTC
    assert current == aware_dt.astimezone(UTC)

    sys_clock: Clock = SystemClock()
    sys_current = sys_clock.now()
    assert sys_current.tzinfo == UTC


@given(
    initial_seconds=st.integers(min_value=1_000_000, max_value=2_000_000_000),
    advance_seconds=st.integers(min_value=-100_000, max_value=100_000),
)
def test_frozen_clock_advance_property(initial_seconds: int, advance_seconds: int) -> None:
    base_dt = datetime.fromtimestamp(initial_seconds, tz=UTC)
    clock = FrozenClock(base_dt)
    delta = timedelta(seconds=advance_seconds)
    clock.advance(delta)
    assert clock.now() == base_dt + delta
