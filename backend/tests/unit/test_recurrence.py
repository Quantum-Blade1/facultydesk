from datetime import date, time
from uuid import uuid4
from zoneinfo import ZoneInfo

from hypothesis import given
from hypothesis import strategies as st

from app.application.calendar.recurrence import expand_slot_recurrence
from app.domain.entities import AcademicTerm, TimetableSlot
from app.domain.value_objects import TimeSlot


@given(
    weekday=st.integers(min_value=0, max_value=6),
    start_hour=st.integers(min_value=8, max_value=16),
    duration_mins=st.integers(min_value=30, max_value=120),
)
def test_recurrence_expansion_matching_weekday(
    weekday: int, start_hour: int, duration_mins: int
) -> None:
    term = AcademicTerm(
        id=uuid4(),
        name="Autumn 2026",
        start_date=date(2026, 8, 1),
        end_date=date(2026, 11, 30),
    )
    start_t = time(start_hour, 0)
    end_mins = start_hour * 60 + duration_mins
    end_t = time(end_mins // 60, end_mins % 60)

    slot = TimetableSlot(
        id=uuid4(),
        time_slot=TimeSlot(weekday, start_t, end_t),
    )

    window_start = date(2026, 9, 1)
    window_end = date(2026, 9, 21)

    occurrences = expand_slot_recurrence(
        slot=slot,
        term=term,
        holidays=set(),
        window_start=window_start,
        window_end=window_end,
    )

    for occ_date, start_utc, end_utc in occurrences:
        assert occ_date.weekday() == weekday
        assert window_start <= occ_date <= window_end
        assert term.start_date <= occ_date <= term.end_date
        assert start_utc < end_utc


def test_recurrence_expansion_skips_holidays() -> None:
    term = AcademicTerm(
        id=uuid4(),
        name="Autumn 2026",
        start_date=date(2026, 8, 1),
        end_date=date(2026, 12, 15),
    )
    slot = TimetableSlot(
        id=uuid4(),
        time_slot=TimeSlot(2, time(10, 0), time(11, 45)),
    )
    holiday_date = date(2026, 10, 28)
    holidays = {holiday_date}

    occurrences = expand_slot_recurrence(
        slot=slot,
        term=term,
        holidays=holidays,
        window_start=date(2026, 10, 26),
        window_end=date(2026, 11, 16),
    )

    occ_dates = [d for d, _, _ in occurrences]
    assert holiday_date not in occ_dates
    assert date(2026, 11, 4) in occ_dates
    assert date(2026, 11, 11) in occ_dates


def test_recurrence_expansion_utc_roundtrip() -> None:
    term = AcademicTerm(
        id=uuid4(),
        name="Autumn 2026",
        start_date=date(2026, 8, 1),
        end_date=date(2026, 12, 15),
    )
    slot = TimetableSlot(
        id=uuid4(),
        time_slot=TimeSlot(2, time(10, 0), time(11, 45)),
    )

    occurrences = expand_slot_recurrence(
        slot=slot,
        term=term,
        holidays=set(),
        window_start=date(2026, 11, 1),
        window_end=date(2026, 11, 15),
    )

    tz_kolkata = ZoneInfo("Asia/Kolkata")
    for occ_date, start_utc, end_utc in occurrences:
        start_local = start_utc.astimezone(tz_kolkata)
        end_local = end_utc.astimezone(tz_kolkata)
        assert start_local.date() == occ_date
        assert start_local.time() == slot.time_slot.start_time
        assert end_local.time() == slot.time_slot.end_time
