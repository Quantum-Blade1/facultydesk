from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from hypothesis import given
from hypothesis import strategies as st

from app.application.calendar.free_slots import BusyInterval, FreeSlotFinder


@given(
    busy_starts=st.lists(
        st.integers(min_value=0, max_value=400),
        min_size=0,
        max_size=10,
    ),
    duration_mins=st.integers(min_value=15, max_value=90),
)
def test_free_slots_never_intersect_busy_property(
    busy_starts: list[int], duration_mins: int
) -> None:
    tz = ZoneInfo("Asia/Kolkata")
    d = date(2026, 10, 27)
    base_local = datetime.combine(d, time(8, 0), tzinfo=tz)
    base_utc = base_local.astimezone(UTC)

    busy_intervals: list[BusyInterval] = []
    for s_min in busy_starts:
        s = base_utc + timedelta(minutes=s_min)
        e = s + timedelta(minutes=30)
        busy_intervals.append(BusyInterval(start_utc=s, end_utc=e))

    finder = FreeSlotFinder(
        work_start_time=time(8, 0),
        work_end_time=time(18, 0),
        timezone_str="Asia/Kolkata",
    )

    free_slots = finder.find_free_slots(
        busy_intervals=busy_intervals,
        start_date=d,
        end_date=d,
        min_duration_minutes=duration_mins,
    )

    for fs in free_slots:
        fs_start, fs_end = fs
        assert (fs_end - fs_start) >= timedelta(minutes=duration_mins)
        for b in busy_intervals:
            overlap = (fs_start < b.end_utc) and (b.start_utc < fs_end)
            assert not overlap


def test_free_slots_worked_example() -> None:
    tz = ZoneInfo("Asia/Kolkata")
    d = date(2026, 10, 27)

    a1_s = datetime.combine(d, time(10, 0), tzinfo=tz).astimezone(UTC)
    a1_e = datetime.combine(d, time(11, 0), tzinfo=tz).astimezone(UTC)

    a2_s = datetime.combine(d, time(14, 0), tzinfo=tz).astimezone(UTC)
    a2_e = datetime.combine(d, time(15, 30), tzinfo=tz).astimezone(UTC)

    b1_s = datetime.combine(d, time(10, 30), tzinfo=tz).astimezone(UTC)
    b1_e = datetime.combine(d, time(12, 0), tzinfo=tz).astimezone(UTC)

    busy = [
        BusyInterval(start_utc=a1_s, end_utc=a1_e),
        BusyInterval(start_utc=a2_s, end_utc=a2_e),
        BusyInterval(start_utc=b1_s, end_utc=b1_e),
    ]

    finder = FreeSlotFinder(
        work_start_time=time(9, 0),
        work_end_time=time(17, 0),
        timezone_str="Asia/Kolkata",
    )

    slots_45 = finder.find_free_slots(
        busy_intervals=busy,
        start_date=d,
        end_date=d,
        min_duration_minutes=45,
    )
    assert len(slots_45) == 3

    slots_90 = finder.find_free_slots(
        busy_intervals=busy,
        start_date=d,
        end_date=d,
        min_duration_minutes=90,
    )
    assert len(slots_90) == 2
