from datetime import UTC, datetime, timedelta
from typing import Protocol


class Clock(Protocol):
    def now(self) -> datetime:
        ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class FrozenClock:
    def __init__(self, current_time: datetime) -> None:
        if current_time.tzinfo is None or current_time.tzinfo.utcoffset(current_time) is None:
            raise ValueError("datetime must be timezone-aware")
        self._current_time: datetime = current_time.astimezone(UTC)

    def now(self) -> datetime:
        return self._current_time

    def set_time(self, new_time: datetime) -> None:
        if new_time.tzinfo is None or new_time.tzinfo.utcoffset(new_time) is None:
            raise ValueError("datetime must be timezone-aware")
        self._current_time = new_time.astimezone(UTC)

    def advance(self, delta: timedelta) -> None:
        self._current_time += delta
