from datetime import UTC, date, datetime, time
from uuid import uuid4

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from app.domain.entities import Event, FacultyProfile
from app.domain.value_objects import EventKind, EventSource, Initials
from app.infrastructure.ocr.duplicate_detector import (
    detect_probable_duplicate,
)
from app.infrastructure.ocr.engine import compute_length_weighted_confidence
from app.infrastructure.ocr.extractor import (
    CircularExtractor,
    parse_meeting_date,
    parse_meeting_time,
)
from app.infrastructure.ocr.preprocessor import compute_deskew_angle


def test_length_weighted_document_confidence() -> None:
    words = ["Meeting", "at", "10:30", "AM", "."]
    confidences = [90.0, 80.0, 95.0, 85.0, 20.0]
    conf = compute_length_weighted_confidence(words, confidences)
    expected = round(1455.0 / 17.0, 2)
    assert conf == expected

    unweighted = sum(confidences) / len(confidences)
    assert unweighted == 74.0
    assert conf > unweighted


@given(
    token_lengths=st.lists(st.integers(min_value=1, max_value=20), min_size=1, max_size=50),
    confidences=st.lists(
        st.floats(min_value=0.0, max_value=100.0, allow_nan=False),
        min_size=1,
        max_size=50,
    ),
)
def test_confidence_bounds_property(token_lengths: list[int], confidences: list[float]) -> None:
    n = min(len(token_lengths), len(confidences))
    words = ["x" * token_lengths[i] for i in range(n)]
    confs = confidences[:n]
    result = compute_length_weighted_confidence(words, confs)
    assert 0.0 <= result <= 100.0


def test_confidence_empty_tokens() -> None:
    assert compute_length_weighted_confidence([], []) == 0.0
    assert compute_length_weighted_confidence(["   "], [90.0]) == 0.0
    assert compute_length_weighted_confidence(["test"], [-1.0]) == 0.0


def test_deskew_skip_sub_threshold() -> None:
    h, w = 200, 400
    img = np.ones((h, w), dtype=np.uint8) * 255
    img[95:105, 50:350] = 0
    angle = compute_deskew_angle(img)
    assert abs(angle) < 0.5


def test_meeting_time_grammar_table() -> None:
    t1 = parse_meeting_time("Meeting at 10:30 AM in Room 101")
    assert t1 is not None
    assert t1.start_time == time(10, 30)
    assert t1.end_time == time(11, 30)
    assert t1.is_assumed_duration is True

    t2 = parse_meeting_time("Commencing at 10.30 am sharp")
    assert t2 is not None
    assert t2.start_time == time(10, 30)
    assert t2.end_time == time(11, 30)
    assert t2.is_assumed_duration is True

    t3 = parse_meeting_time("Reporting time 1030 hrs in seminar hall")
    assert t3 is not None
    assert t3.start_time == time(10, 30)
    assert t3.end_time == time(11, 30)
    assert t3.is_assumed_duration is True

    t4 = parse_meeting_time("Session scheduled from 2 pm to 4 pm today")
    assert t4 is not None
    assert t4.start_time == time(14, 0)
    assert t4.end_time == time(16, 0)
    assert t4.is_assumed_duration is False

    t5 = parse_meeting_time("Meeting duration: 14:00-15:30")
    assert t5 is not None
    assert t5.start_time == time(14, 0)
    assert t5.end_time == time(15, 30)
    assert t5.is_assumed_duration is False


def test_meeting_date_extraction_cues() -> None:
    text = "Ref: FD/2026/01. Dated: 2026-10-15. Meeting on 28-10-2026 at Board Room."
    parsed_date, conf = parse_meeting_date(text)
    assert parsed_date == date(2026, 10, 28)
    assert conf == 1.0


def test_duplicate_predicate_worked_example() -> None:
    ev = Event(
        id=uuid4(),
        title="Board of Studies Meeting",
        kind=EventKind.MEETING,
        start_utc=datetime(2026, 11, 5, 5, 0, tzinfo=UTC),
        end_utc=datetime(2026, 11, 5, 6, 0, tzinfo=UTC),
        location="Board Room",
        source=EventSource.CIRCULAR,
    )

    is_dup, dup_id = detect_probable_duplicate(
        candidate_title="Sub: Board of Studies Meeting in CSE",
        candidate_date=date(2026, 11, 5),
        candidate_start_time=time(10, 30),
        existing_events=[ev],
    )
    assert is_dup is True
    assert dup_id == ev.id

    is_dup2, _ = detect_probable_duplicate(
        candidate_title="Sub: Board of Studies Meeting in CSE",
        candidate_date=date(2026, 11, 6),
        candidate_start_time=time(10, 30),
        existing_events=[ev],
    )
    assert is_dup2 is False


def test_review_gate_decision_matrix() -> None:
    extractor = CircularExtractor(doc_confidence_threshold=70.0, name_confidence_threshold=0.85)
    dept_id = uuid4()
    p1 = FacultyProfile(
        id=uuid4(),
        department_id=dept_id,
        full_name="Krish Kumar Sharma",
        initials=Initials("KKS"),
    )

    valid_text = (
        "Sub: Department Meeting\n"
        "Meeting on 15-11-2026 at 10:30 AM in Board Room\n"
        "Agenda:\n"
        "1. Curriculum revision\n"
        "Attendees: KKS\n"
    )
    res_pass = extractor.extract(
        text=valid_text,
        document_confidence=85.0,
        faculty_profiles=[p1],
        is_probable_duplicate=False,
    )
    assert res_pass.is_auto_confirmable is True
    assert len(res_pass.review_reasons) == 0

    res_low_doc = extractor.extract(
        text=valid_text,
        document_confidence=55.0,
        faculty_profiles=[p1],
        is_probable_duplicate=False,
    )
    assert res_low_doc.is_auto_confirmable is False
    assert "LOW_DOCUMENT_CONFIDENCE" in res_low_doc.review_reasons

    no_date_text = "Sub: Department Meeting\nMeeting at 10:30 AM in Board Room\nAttendees: KKS\n"
    res_no_date = extractor.extract(
        text=no_date_text,
        document_confidence=85.0,
        faculty_profiles=[p1],
        is_probable_duplicate=False,
    )
    assert res_no_date.is_auto_confirmable is False
    assert "MISSING_OR_UNCERTAIN_DATE" in res_no_date.review_reasons
