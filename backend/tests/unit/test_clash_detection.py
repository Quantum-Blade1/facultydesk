from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from hypothesis import given
from hypothesis import strategies as st

from app.application.calendar.clash_detector import (
    Interval,
    SweepLineClashDetector,
    pairwise_clashes,
)


@given(
    intervals=st.lists(
        st.tuples(
            st.integers(min_value=0, max_value=1000),
            st.integers(min_value=1, max_value=200),
        ),
        min_size=0,
        max_size=40,
    )
)
def test_sweep_line_clash_detection_matches_pairwise_property(
    intervals: list[tuple[int, int]],
) -> None:
    base = datetime(2026, 10, 27, 0, 0, tzinfo=UTC)
    parsed_intervals: list[Interval] = []
    for start_mins, duration_mins in intervals:
        start_utc = base + timedelta(minutes=start_mins)
        end_utc = start_utc + timedelta(minutes=duration_mins)
        parsed_intervals.append(
            Interval(
                id=uuid4(),
                start_utc=start_utc,
                end_utc=end_utc,
            )
        )

    detector = SweepLineClashDetector()
    sweep_clashes = detector.detect_clashes(parsed_intervals)
    brute_clashes = pairwise_clashes(parsed_intervals)

    sweep_set = {
        (min(a, b, key=lambda u: u.bytes), max(a, b, key=lambda u: u.bytes))
        for a, b in sweep_clashes
    }
    brute_set = {
        (min(a, b, key=lambda u: u.bytes), max(a, b, key=lambda u: u.bytes))
        for a, b in brute_clashes
    }
    assert sweep_set == brute_set


@given(
    start_min=st.integers(min_value=0, max_value=500),
    dur1=st.integers(min_value=1, max_value=120),
    dur2=st.integers(min_value=1, max_value=120),
)
def test_adjacent_intervals_no_clash(start_min: int, dur1: int, dur2: int) -> None:
    base = datetime(2026, 10, 27, 8, 0, tzinfo=UTC)
    s1 = base + timedelta(minutes=start_min)
    m = s1 + timedelta(minutes=dur1)
    e2 = m + timedelta(minutes=dur2)

    i1 = Interval(id=uuid4(), start_utc=s1, end_utc=m)
    i2 = Interval(id=uuid4(), start_utc=m, end_utc=e2)

    detector = SweepLineClashDetector()
    clashes = detector.detect_clashes([i1, i2])
    assert len(clashes) == 0


def test_worked_example_from_maths_md() -> None:
    base = datetime(2026, 10, 27, 0, 0, tzinfo=UTC)
    id1 = uuid4()
    id2 = uuid4()
    id3 = uuid4()
    id4 = uuid4()

    e1 = Interval(
        id=id1,
        start_utc=base + timedelta(hours=9),
        end_utc=base + timedelta(hours=10),
    )
    e2 = Interval(
        id=id2,
        start_utc=base + timedelta(hours=9, minutes=30),
        end_utc=base + timedelta(hours=10, minutes=30),
    )
    e3 = Interval(
        id=id3,
        start_utc=base + timedelta(hours=10),
        end_utc=base + timedelta(hours=11),
    )
    e4 = Interval(
        id=id4,
        start_utc=base + timedelta(hours=10, minutes=15),
        end_utc=base + timedelta(hours=10, minutes=45),
    )

    detector = SweepLineClashDetector()
    clashes = detector.detect_clashes([e1, e2, e3, e4])

    clash_pairs = {
        (min(a, b, key=lambda u: u.bytes), max(a, b, key=lambda u: u.bytes))
        for a, b in clashes
    }

    def canonical_pair(u1: UUID, u2: UUID) -> tuple[UUID, UUID]:
        return (min(u1, u2, key=lambda u: u.bytes), max(u1, u2, key=lambda u: u.bytes))


    expected = {
        canonical_pair(id1, id2),
        canonical_pair(id2, id3),
        canonical_pair(id2, id4),
        canonical_pair(id3, id4),
    }

    assert clash_pairs == expected
