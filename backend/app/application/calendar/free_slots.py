from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class BusyInterval:
    start_utc: datetime
    end_utc: datetime


def merge_busy_intervals(intervals: Sequence[BusyInterval]) -> list[BusyInterval]:
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda x: (x.start_utc, x.end_utc))
    merged: list[BusyInterval] = [sorted_intervals[0]]

    for current in sorted_intervals[1:]:
        prev = merged[-1]
        if current.start_utc <= prev.end_utc:
            merged[-1] = BusyInterval(
                start_utc=prev.start_utc,
                end_utc=max(prev.end_utc, current.end_utc),
            )
        else:
            merged.append(current)

    return merged


class FreeSlotFinder:
    def __init__(
        self,
        work_start_time: time = time(8, 0),
        work_end_time: time = time(18, 0),
        timezone_str: str = "Asia/Kolkata",
    ) -> None:
        self._work_start_time = work_start_time
        self._work_end_time = work_end_time
        self._timezone = ZoneInfo(timezone_str)

    def find_free_slots(
        self,
        busy_intervals: Sequence[BusyInterval],
        start_date: date,
        end_date: date,
        min_duration_minutes: int,
    ) -> list[tuple[datetime, datetime]]:
        min_delta = timedelta(minutes=min_duration_minutes)
        merged = merge_busy_intervals(busy_intervals)
        free_slots: list[tuple[datetime, datetime]] = []

        curr = start_date
        while curr <= end_date:
            ws_local = datetime.combine(curr, self._work_start_time, tzinfo=self._timezone)
            we_local = datetime.combine(curr, self._work_end_time, tzinfo=self._timezone)
            w_start = ws_local.astimezone(UTC)
            w_end = we_local.astimezone(UTC)

            day_busy: list[tuple[datetime, datetime]] = []
            for b in merged:
                if b.start_utc < w_end and b.end_utc > w_start:
                    day_busy.append((max(b.start_utc, w_start), min(b.end_utc, w_end)))

            cursor = w_start
            for bs, be in day_busy:
                if bs > cursor and (bs - cursor) >= min_delta:
                    free_slots.append((cursor, bs))
                cursor = max(cursor, be)

            if cursor < w_end and (w_end - cursor) >= min_delta:
                free_slots.append((cursor, w_end))

            curr += timedelta(days=1)

        return free_slots
