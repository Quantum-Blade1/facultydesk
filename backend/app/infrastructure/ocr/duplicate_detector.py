import re
from datetime import date, time
from uuid import UUID
from zoneinfo import ZoneInfo

from rapidfuzz import fuzz

from app.domain.entities import Event


def normalize_title(title: str) -> str:
    cleaned = re.sub(r"^(?:sub|subject|circular|ref)\s*[:\-]\s*", "", title, flags=re.IGNORECASE)
    cleaned = re.sub(r"\b(?:dr|prof|mr|ms|mrs)\b\.?", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[^\w\s]", " ", cleaned)
    return " ".join(cleaned.lower().split())


def detect_probable_duplicate(
    candidate_title: str,
    candidate_date: date,
    candidate_start_time: time,
    existing_events: list[Event],
) -> tuple[bool, UUID | None]:
    tz = ZoneInfo("Asia/Kolkata")
    norm_candidate = normalize_title(candidate_title)

    for ev in existing_events:
        ev_local = ev.start_utc.astimezone(tz)
        if ev_local.date() != candidate_date:
            continue

        ev_time = ev_local.time()
        diff_minutes = abs(
            (ev_time.hour * 60 + ev_time.minute)
            - (candidate_start_time.hour * 60 + candidate_start_time.minute)
        )
        if diff_minutes > 15:
            continue

        norm_ev = normalize_title(ev.title)
        sim = fuzz.token_set_ratio(norm_candidate, norm_ev)
        if sim >= 80:
            return True, ev.id

    return False, None
