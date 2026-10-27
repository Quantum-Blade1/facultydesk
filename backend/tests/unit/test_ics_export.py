from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

import icalendar

from app.application.calendar.ics_service import generate_vcalendar_ics
from app.domain.entities import Event
from app.domain.value_objects import EventKind, EventSource


def test_ics_export_valid_rfc5545() -> None:
    now_utc = datetime(2026, 10, 27, 10, 0, tzinfo=UTC)
    ev1 = Event(
        id=uuid4(),
        kind=EventKind.CLASS,
        title="CN (KKS)",
        start_utc=now_utc + timedelta(days=1),
        end_utc=now_utc + timedelta(days=1, hours=1),
        location="LH-101",
        source=EventSource.TIMETABLE,
        source_id=uuid4(),
        recurrence_date=date(2026, 10, 28),
    )
    ev2 = Event(
        id=uuid4(),
        kind=EventKind.MEETING,
        title="Department Review",
        start_utc=now_utc + timedelta(days=2),
        end_utc=now_utc + timedelta(days=2, hours=2),
        location="Seminar Hall",
        source=EventSource.MANUAL,
    )

    ics_content = generate_vcalendar_ics(
        events=[ev1, ev2],
        calendar_name="FacultyDesk Schedule",
        timestamp_utc=now_utc,
    )

    assert isinstance(ics_content, bytes)
    cal = icalendar.Calendar.from_ical(ics_content)
    assert cal.get("prodid") is not None
    assert cal.get("version") == "2.0"

    subcomponents = [c for c in cal.subcomponents if c.name == "VEVENT"]
    assert len(subcomponents) == 2

    e1 = subcomponents[0]
    assert "slot-" in str(e1.get("uid"))
    assert str(e1.get("summary")) == "CN (KKS)"
    assert str(e1.get("location")) == "LH-101"

    e2 = subcomponents[1]
    assert "event-" in str(e2.get("uid"))
    assert str(e2.get("summary")) == "Department Review"


def test_ics_export_stable_uids() -> None:
    now_utc = datetime(2026, 10, 27, 10, 0, tzinfo=UTC)
    slot_id = uuid4()
    occ_date = date(2026, 11, 4)

    ev = Event(
        id=uuid4(),
        kind=EventKind.CLASS,
        title="DBMS Lab",
        start_utc=now_utc,
        end_utc=now_utc + timedelta(hours=2),
        location="Lab 3",
        source=EventSource.TIMETABLE,
        source_id=slot_id,
        recurrence_date=occ_date,
    )

    ics_1 = generate_vcalendar_ics([ev], timestamp_utc=now_utc)
    ics_2 = generate_vcalendar_ics([ev], timestamp_utc=now_utc + timedelta(hours=1))

    cal1 = icalendar.Calendar.from_ical(ics_1)
    cal2 = icalendar.Calendar.from_ical(ics_2)

    uid1 = str(cal1.subcomponents[0].get("uid"))
    uid2 = str(cal2.subcomponents[0].get("uid"))

    assert uid1 == uid2
    assert uid1 == f"slot-{slot_id}-{occ_date.isoformat()}@facultydesk.local"
