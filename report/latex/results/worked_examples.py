import json
import random
import sys
import time
from datetime import UTC, datetime, timedelta
from datetime import time as clock_time
from pathlib import Path
from uuid import uuid4

from app.application.calendar.clash_detector import (
    Interval,
    SweepLineClashDetector,
    pairwise_clashes,
)
from app.application.reminders.maths import adjust_for_quiet_hours, compute_fire_time
from app.application.tasks.maths import compute_lead_alert_times, compute_priority_score
from app.domain.value_objects import QuietHours
from app.infrastructure.ocr.engine import compute_length_weighted_confidence
from app.infrastructure.parsers.initials_resolver import normalized_similarity

SEED = 20261113
NOW = datetime(2026, 11, 13, 4, 30, tzinfo=UTC)


def priority_examples() -> list[dict[str, object]]:
    cases = [
        ("IA marks upload", 5, timedelta(hours=6)),
        ("CO-PO mapping", 4, timedelta(hours=48)),
        ("Lab manual update", 2, timedelta(days=10)),
        ("Course file submission", 3, timedelta(hours=-36)),
    ]
    return [
        {
            "task": title,
            "importance": imp,
            "hours_to_deadline": round(delta.total_seconds() / 3600, 1),
            "score": compute_priority_score(imp, NOW + delta, NOW),
        }
        for title, imp, delta in cases
    ]


def similarity_examples() -> list[dict[str, object]]:
    pairs = [("KKS", "KKS"), ("KKS", "KSS"), ("PARKAVI", "PARKAVY"), ("RNS", "KKS")]
    return [{"a": a, "b": b, "similarity": round(normalized_similarity(a, b), 4)} for a, b in pairs]


def quiet_hours_example() -> dict[str, str]:
    quiet = QuietHours(start_time=clock_time(22, 0), end_time=clock_time(7, 0))
    event_start = datetime(2026, 11, 14, 4, 30, tzinfo=UTC)
    fire = compute_fire_time(event_start, 12 * 60)
    shifted = adjust_for_quiet_hours(fire, event_start, quiet)
    return {
        "event_start_utc": event_start.isoformat(),
        "raw_fire_utc": fire.isoformat(),
        "shifted_fire_utc": shifted.isoformat(),
    }


def task_alert_example() -> list[str]:
    deadline = NOW + timedelta(days=5)
    return [t.isoformat() for t in compute_lead_alert_times(deadline, NOW)]


def confidence_example() -> float:
    words = ["Meeting", "on", "18/11/2026", "at", "2:30", "PM"]
    confidences = [96.0, 91.0, 72.0, 88.0, 65.0, 90.0]
    return round(compute_length_weighted_confidence(words, confidences), 4)


def clash_benchmark(n: int, rng: random.Random) -> dict[str, object]:
    base = datetime(2026, 11, 16, 3, 0, tzinfo=UTC)
    intervals = []
    for _ in range(n):
        start = base + timedelta(minutes=rng.randrange(0, 60 * 24 * 30, 15))
        intervals.append(Interval(uuid4(), start, start + timedelta(minutes=rng.choice([50, 60, 120]))))
    t0 = time.perf_counter()
    sweep = SweepLineClashDetector().detect_clashes(intervals)
    t1 = time.perf_counter()
    brute = pairwise_clashes(intervals)
    t2 = time.perf_counter()
    same = {frozenset(p) for p in sweep} == {frozenset(p) for p in brute}
    return {
        "n": n,
        "clash_pairs": len(sweep),
        "sweep_ms": round((t1 - t0) * 1000, 2),
        "pairwise_ms": round((t2 - t1) * 1000, 2),
        "results_identical": same,
    }


def main() -> None:
    rng = random.Random(SEED)
    out = {
        "seed": SEED,
        "now_utc": NOW.isoformat(),
        "python": sys.version.split()[0],
        "priority": priority_examples(),
        "similarity": similarity_examples(),
        "quiet_hours": quiet_hours_example(),
        "task_alerts": task_alert_example(),
        "ocr_confidence": confidence_example(),
        "clash_benchmark": [clash_benchmark(n, rng) for n in (500, 1000, 2000, 4000)],
    }
    target = Path(sys.argv[1])
    target.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
