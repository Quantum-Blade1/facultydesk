from collections.abc import Sequence
from datetime import UTC, datetime

import icalendar

from app.domain.entities import Event
from app.domain.value_objects import EventSource


def generate_vcalendar_ics(
    events: Sequence[Event],
    calendar_name: str = "FacultyDesk Schedule",
    timestamp_utc: datetime | None = None,
) -> bytes:
    cal = icalendar.Calendar()
    cal.add("prodid", "-//FacultyDesk//Academic Calendar//EN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("method", "PUBLISH")
    cal.add("x-wr-calname", calendar_name)
    cal.add("x-wr-timezone", "UTC")

    dtstamp = timestamp_utc if timestamp_utc is not None else datetime.now(UTC)

    for ev in events:
        vevent = icalendar.Event()
        if (
            ev.source == EventSource.TIMETABLE
            and ev.source_id is not None
            and ev.recurrence_date is not None
        ):
            uid = f"slot-{ev.source_id}-{ev.recurrence_date.isoformat()}@facultydesk.local"
        else:
            uid = f"event-{ev.id}@facultydesk.local"

        vevent.add("uid", uid)
        vevent.add("dtstamp", dtstamp)
        vevent.add("dtstart", ev.start_utc)
        vevent.add("dtend", ev.end_utc)
        vevent.add("summary", ev.title)
        if ev.location:
            vevent.add("location", ev.location)
        vevent.add("status", "CONFIRMED")

        cal.add_component(vevent)

    raw_bytes: bytes = cal.to_ical()
    return raw_bytes
