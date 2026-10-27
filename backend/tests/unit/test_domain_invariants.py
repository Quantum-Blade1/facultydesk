import itertools
from datetime import UTC, datetime, time, timedelta

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain import (
    Circular,
    CircularStatus,
    Event,
    EventKind,
    EventSource,
    Initials,
    InvalidTransition,
    InvariantViolation,
    NotificationStatus,
    QuietHours,
    ScheduledNotification,
    Task,
    TimeSlot,
)


@given(st.from_regex(r"\A[A-Z]{2,5}\Z"))
def test_initials_valid_property(val: str) -> None:
    initials = Initials(val)
    assert initials.value == val
    assert str(initials) == val


def _is_valid_initials_string(s: str) -> bool:
    return 2 <= len(s) <= 5 and s.isupper() and s.isalpha() and "\n" not in s


@given(st.text().filter(lambda s: not _is_valid_initials_string(s)))
def test_initials_invalid_property(val: str) -> None:
    with pytest.raises(InvariantViolation):
        Initials(val)


def test_timeslot_invariants() -> None:
    slot = TimeSlot(0, time(9, 0), time(10, 0))
    assert slot.weekday == 0

    with pytest.raises(InvariantViolation):
        TimeSlot(7, time(9, 0), time(10, 0))

    with pytest.raises(InvariantViolation):
        TimeSlot(-1, time(9, 0), time(10, 0))

    with pytest.raises(InvariantViolation):
        TimeSlot(0, time(10, 0), time(9, 0))

    with pytest.raises(InvariantViolation):
        TimeSlot(0, time(10, 0), time(10, 0))


def test_timeslot_half_open_overlap() -> None:
    slot1 = TimeSlot(1, time(9, 0), time(10, 0))
    slot2 = TimeSlot(1, time(10, 0), time(11, 0))
    slot3 = TimeSlot(1, time(9, 30), time(10, 30))
    slot_diff_day = TimeSlot(2, time(9, 30), time(10, 30))

    assert not slot1.overlaps(slot2)
    assert not slot2.overlaps(slot1)
    assert slot1.overlaps(slot3)
    assert slot3.overlaps(slot1)
    assert not slot1.overlaps(slot_diff_day)


def test_quiet_hours_midnight_crossing() -> None:
    qh = QuietHours(time(22, 0), time(7, 0))
    assert qh.crosses_midnight
    assert qh.covers(time(23, 0))
    assert qh.covers(time(6, 30))
    assert not qh.covers(time(12, 0))
    assert not qh.covers(time(7, 0))
    assert qh.covers(time(22, 0))

    standard = QuietHours(time(13, 0), time(14, 0))
    assert not standard.crosses_midnight
    assert standard.covers(time(13, 30))
    assert not standard.covers(time(12, 0))
    assert not standard.covers(time(14, 0))


def test_event_invariants() -> None:
    now = datetime.now(UTC)
    ev = Event(
        kind=EventKind.CLASS,
        title="Operating Systems",
        start_utc=now,
        end_utc=now + timedelta(hours=1),
        location="Room 301",
        source=EventSource.TIMETABLE,
    )
    assert ev.title == "Operating Systems"

    with pytest.raises(InvariantViolation):
        Event(
            kind=EventKind.CLASS,
            title="",
            start_utc=now,
            end_utc=now + timedelta(hours=1),
        )

    with pytest.raises(InvariantViolation):
        Event(
            kind=EventKind.CLASS,
            title="Class",
            start_utc=now,
            end_utc=now - timedelta(hours=1),
        )

    with pytest.raises(InvariantViolation):
        Event(
            kind=EventKind.CLASS,
            title="Class",
            start_utc=datetime.now(),
            end_utc=datetime.now() + timedelta(hours=1),
        )


def test_event_reschedule() -> None:
    now = datetime.now(UTC)
    ev = Event(
        kind=EventKind.MEETING,
        title="Faculty Meeting",
        start_utc=now,
        end_utc=now + timedelta(hours=1),
    )
    new_start = now + timedelta(days=1)
    new_end = new_start + timedelta(hours=2)
    ev.reschedule(new_start, new_end)
    assert ev.start_utc == new_start
    assert ev.end_utc == new_end
    assert len(ev.domain_events) == 1


def test_circular_state_machine_exhaustive() -> None:
    all_states = list(CircularStatus)
    valid_transitions = {
        (CircularStatus.UPLOADED, CircularStatus.PROCESSING),
        (CircularStatus.PROCESSING, CircularStatus.NEEDS_REVIEW),
        (CircularStatus.PROCESSING, CircularStatus.CONFIRMED),
        (CircularStatus.PROCESSING, CircularStatus.FAILED),
        (CircularStatus.NEEDS_REVIEW, CircularStatus.CONFIRMED),
        (CircularStatus.NEEDS_REVIEW, CircularStatus.REJECTED),
        (CircularStatus.FAILED, CircularStatus.PROCESSING),
    }

    assert len(valid_transitions) == 7
    total_pairs = list(itertools.product(all_states, all_states))
    assert len(total_pairs) == 36

    for s_from, s_to in total_pairs:
        circ = Circular(status=s_from)
        if (s_from, s_to) in valid_transitions:
            circ._transition(s_to)
            assert circ.status == s_to
        else:
            with pytest.raises(InvalidTransition):
                circ._transition(s_to)


def test_notification_state_machine_exhaustive() -> None:
    all_states = list(NotificationStatus)
    valid_transitions = {
        (NotificationStatus.PENDING, NotificationStatus.SENDING),
        (NotificationStatus.SENDING, NotificationStatus.SENT),
        (NotificationStatus.SENDING, NotificationStatus.FAILED),
        (NotificationStatus.FAILED, NotificationStatus.PENDING),
        (NotificationStatus.PENDING, NotificationStatus.CANCELLED),
    }

    assert len(valid_transitions) == 5
    total_pairs = list(itertools.product(all_states, all_states))
    assert len(total_pairs) == 25

    for s_from, s_to in total_pairs:
        notif = ScheduledNotification(status=s_from)
        if (s_from, s_to) in valid_transitions:
            notif._transition(s_to)
            assert notif.status == s_to
        else:
            with pytest.raises(InvalidTransition):
                notif._transition(s_to)


def test_task_invariants() -> None:
    now = datetime.now(UTC)
    task = Task(
        title="CO-PO Mapping",
        deadline_utc=now + timedelta(days=7),
        importance=4,
    )
    assert task.importance == 4

    with pytest.raises(InvariantViolation):
        Task(
            title="",
            deadline_utc=now,
            importance=3,
        )

    with pytest.raises(InvariantViolation):
        Task(
            title="Invalid",
            deadline_utc=now,
            importance=6,
        )

    with pytest.raises(InvariantViolation):
        Task(
            title="Invalid",
            deadline_utc=now,
            importance=0,
        )
