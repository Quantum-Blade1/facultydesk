import re
from datetime import time

WEEKDAY_MAP: dict[str, int] = {
    "mon": 1,
    "monday": 1,
    "tue": 2,
    "tues": 2,
    "tuesday": 2,
    "wed": 3,
    "wednesday": 3,
    "thu": 4,
    "thur": 4,
    "thurs": 4,
    "thursday": 4,
    "fri": 5,
    "friday": 5,
    "sat": 6,
    "saturday": 6,
    "sun": 7,
    "sunday": 7,
}

TIME_RANGE_REGEX = re.compile(
    r"^\s*(\d{1,2})[:.](\d{2})\s*(am|pm)?\s*(?:-|to|\u2013)\s*(\d{1,2})[:.](\d{2})\s*(am|pm)?\s*$",
    re.IGNORECASE,
)


def normalize_weekday(token: str) -> int | None:
    cleaned = token.strip().lower()
    return WEEKDAY_MAP.get(cleaned)


def _adjust_hour(hour: int, meridian: str | None) -> int:
    if meridian is None:
        return hour
    norm = meridian.lower()
    if norm == "pm" and hour < 12:
        return hour + 12
    if norm == "am" and hour == 12:
        return 0
    return hour


def parse_time_range(token: str) -> tuple[time, time] | None:
    match = TIME_RANGE_REGEX.match(token)
    if not match:
        return None

    h1_str, m1_str, mer1, h2_str, m2_str, mer2 = match.groups()
    h1, m1 = int(h1_str), int(m1_str)
    h2, m2 = int(h2_str), int(m2_str)

    if not (0 <= m1 < 60 and 0 <= m2 < 60):
        return None

    if mer1 is None and mer2 is not None:
        if mer2.lower() == "pm" and h1 < 12 and h1 > h2:
            mer1 = "am"
        elif mer2.lower() == "pm" and h1 < 12 and h1 <= h2:
            mer1 = "pm"
        else:
            mer1 = mer2

    h1 = _adjust_hour(h1, mer1)
    h2 = _adjust_hour(h2, mer2)

    if mer1 is None and mer2 is None:
        if 1 <= h1 <= 6:
            h1 += 12
        if 1 <= h2 <= 6:
            h2 += 12

    if not (0 <= h1 < 24 and 0 <= h2 < 24):
        return None

    return time(h1, m1), time(h2, m2)
