from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

from dateutil.rrule import FR, MO, SA, SU, TH, TU, WE, WEEKLY, rrule

from app.domain.entities import AcademicTerm, TimetableSlot

WEEKDAY_MAP = [MO, TU, WE, TH, FR, SA, SU]


def expand_slot_recurrence(
    slot: TimetableSlot,
    term: AcademicTerm,
    holidays: set[date],
    window_start: date,
    window_end: date,
) -> list[tuple[date, datetime, datetime]]:
    effective_start = max(term.start_date, window_start)
    effective_end = min(term.end_date, window_end)

    if effective_start > effective_end:
        return []

    rrule_weekday = WEEKDAY_MAP[slot.time_slot.weekday]
    dtstart = datetime.combine(effective_start, slot.time_slot.start_time)
    until = datetime.combine(effective_end, slot.time_slot.end_time)

    rule = rrule(
        WEEKLY,
        dtstart=dtstart,
        until=until,
        byweekday=rrule_weekday,
    )

    tz = ZoneInfo(term.timezone)
    occurrences: list[tuple[date, datetime, datetime]] = []

    for dt in rule:
        occ_date = dt.date()
        if occ_date in holidays:
            continue
        if occ_date < effective_start or occ_date > effective_end:
            continue

        start_local = datetime.combine(occ_date, slot.time_slot.start_time, tzinfo=tz)
        end_local = datetime.combine(occ_date, slot.time_slot.end_time, tzinfo=tz)

        start_utc = start_local.astimezone(UTC)
        end_utc = end_local.astimezone(UTC)

        occurrences.append((occ_date, start_utc, end_utc))

    return occurrences
