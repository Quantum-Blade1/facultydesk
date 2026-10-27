import re
from dataclasses import dataclass
from datetime import date, time
from uuid import UUID

import dateparser
from rapidfuzz import fuzz

from app.domain.entities import FacultyProfile


@dataclass(frozen=True)
class ExtractedTime:
    start_time: time
    end_time: time
    is_assumed_duration: bool
    confidence: float


@dataclass(frozen=True)
class ExtractedAttendee:
    faculty_id: UUID
    full_name: str
    initials: str
    confidence: float
    match_type: str


@dataclass(frozen=True)
class ExtractionResult:
    title: str
    agenda: list[str]
    meeting_date: date | None
    date_confidence: float
    extracted_time: ExtractedTime | None
    venue: str
    venue_confidence: float
    attendees: list[ExtractedAttendee]
    is_all_faculty: bool
    review_reasons: list[str]
    is_auto_confirmable: bool


def parse_military_time(text: str) -> time | None:
    m = re.search(r"\b([01]?\d|2[0-3])([0-5]\d)\s*(?:hrs|hours|HRS)\b", text)
    if m:
        h = int(m.group(1))
        minute = int(m.group(2))
        return time(h, minute)
    return None


def _to_24h(h: int, minute: int, meridiem: str | None) -> time:
    if meridiem:
        lower_m = meridiem.lower().replace(".", "")
        if lower_m == "pm" and h < 12:
            h += 12
        elif lower_m == "am" and h == 12:
            h = 0
    else:
        if h < 8:
            h += 12
    return time(h, minute)


def parse_meeting_time(text: str) -> ExtractedTime | None:
    interval_pat = (
        r"\b([01]?\d|2[0-3])(?:[:.](\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?\s*"
        r"(?:-|to|until|--)\s*"
        r"([01]?\d|2[0-3])(?:[:.](\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?\b"
    )
    match_interval = re.search(interval_pat, text, re.IGNORECASE)
    if match_interval:
        h1 = int(match_interval.group(1))
        m1 = int(match_interval.group(2)) if match_interval.group(2) else 0
        mer1 = match_interval.group(3)

        h2 = int(match_interval.group(4))
        m2 = int(match_interval.group(5)) if match_interval.group(5) else 0
        mer2 = match_interval.group(6)

        if not mer1 and mer2:
            mer1 = mer2

        t1 = _to_24h(h1, m1, mer1)
        t2 = _to_24h(h2, m2, mer2)
        if t2 <= t1 and t2.hour < 12:
            t2 = time(t2.hour + 12, t2.minute)

        return ExtractedTime(
            start_time=t1,
            end_time=t2,
            is_assumed_duration=False,
            confidence=1.0,
        )

    t_mil = parse_military_time(text)
    if t_mil:
        end_h = (t_mil.hour + 1) % 24
        t_end = time(end_h, t_mil.minute)
        return ExtractedTime(
            start_time=t_mil,
            end_time=t_end,
            is_assumed_duration=True,
            confidence=0.85,
        )

    single_pat = r"\b([01]?\d|2[0-3])[:.](\d{2})\s*(am|pm|a\.m\.|p\.m\.)?\b"
    match_single = re.search(single_pat, text, re.IGNORECASE)
    if match_single:
        h = int(match_single.group(1))
        minute = int(match_single.group(2))
        mer = match_single.group(3)
        t_start = _to_24h(h, minute, mer)
        end_h = (t_start.hour + 1) % 24
        t_end = time(end_h, t_start.minute)
        return ExtractedTime(
            start_time=t_start,
            end_time=t_end,
            is_assumed_duration=True,
            confidence=0.85,
        )

    return None


def parse_meeting_date(text: str) -> tuple[date | None, float]:
    date_settings = {
        "DATE_ORDER": "DMY",
        "PREFER_DATES_FROM": "future",
        "TIMEZONE": "Asia/Kolkata",
    }

    cue_patterns = [
        r"(?:meeting\s+(?:on|held\s+on|scheduled\s+on)|held\s+on|scheduled\s+on|on\s+date)\s*[:\-]?\s*([0-9]{1,2}[./-][0-9]{1,2}[./-][0-9]{2,4})",
        r"(?:meeting\s+(?:on|held\s+on|scheduled\s+on)|held\s+on|scheduled\s+on|on\s+date)\s*[:\-]?\s*([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{2,4})",
    ]

    for pat in cue_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            raw_str = m.group(1).strip()
            parsed = dateparser.parse(raw_str, settings=date_settings)
            if parsed:
                return parsed.date(), 1.0

    raw_candidates = re.findall(r"\b([0-9]{1,2}[./-][0-9]{1,2}[./-][0-9]{2,4})\b", text)
    for c in reversed(raw_candidates):
        parsed = dateparser.parse(c, settings=date_settings)
        if parsed:
            return parsed.date(), 0.85

    return None, 0.0


def parse_venue(text: str) -> tuple[str, float]:
    cues = [
        r"(?:in\s+the|venue\s*[:\-]?|place\s*[:\-]?|hall\s*[:\-]?|room\s*[:\-]?)\s*([A-Za-z0-9\s]+(?:Hall|Room|Lab|Center|Auditorium|Auditorium\s+\d+|Lab\s+\d+|Room\s+\d+))",
        r"\b(Seminar\s+Hall|Board\s+Room|Conference\s+Room|Auditorium|Computer\s+Center(?:\s+Lab\s+\d+)?|Room\s+\d+)\b",
    ]
    for pat in cues:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            venue_str = m.group(1).strip()
            return venue_str, 0.95
    return "Department Meeting Room", 0.50


def parse_title_and_agenda(text: str) -> tuple[str, list[str]]:
    title = "Department Meeting"
    for line in text.splitlines():
        clean = line.strip()
        if re.match(r"^(?:Sub|Subject)\s*[:\-]\s*(.+)", clean, re.IGNORECASE):
            sub_m = re.match(r"^(?:Sub|Subject)\s*[:\-]\s*(.+)", clean, re.IGNORECASE)
            if sub_m:
                title = sub_m.group(1).strip()
                break
        elif re.match(r"^CIRCULAR\s*[:\-]?\s*(.+)", clean, re.IGNORECASE):
            c_m = re.match(r"^CIRCULAR\s*[:\-]?\s*(.+)", clean, re.IGNORECASE)
            if c_m and len(c_m.group(1).strip()) > 5:
                title = c_m.group(1).strip()

    agenda_items: list[str] = []
    for line in text.splitlines():
        clean = line.strip()
        m_item = re.match(r"^\d+\.\s*(.+)", clean)
        if m_item:
            agenda_items.append(m_item.group(1).strip())

    return title, agenda_items


def resolve_circular_attendees(
    text: str,
    faculty_profiles: list[FacultyProfile],
) -> tuple[list[ExtractedAttendee], bool]:
    lower_text = text.lower()
    if "all faculty" in lower_text or "all staff" in lower_text:
        all_att = [
            ExtractedAttendee(
                faculty_id=p.id,
                full_name=p.full_name,
                initials=p.initials.value,
                confidence=1.0,
                match_type="ALL_FACULTY",
            )
            for p in faculty_profiles
        ]
        return all_att, True

    extracted: dict[UUID, ExtractedAttendee] = {}

    initials_map: dict[str, FacultyProfile] = {}
    alias_map: dict[str, FacultyProfile] = {}
    for p in faculty_profiles:
        initials_map[p.initials.value.upper()] = p
        for alias in p.aliases:
            alias_map[alias.upper()] = p

    tokens = re.findall(r"\b([A-Z]{2,4})\b", text)
    for t in tokens:
        if t in initials_map:
            p = initials_map[t]
            if p.id not in extracted:
                extracted[p.id] = ExtractedAttendee(
                    faculty_id=p.id,
                    full_name=p.full_name,
                    initials=p.initials.value,
                    confidence=1.0,
                    match_type="EXACT_INITIALS",
                )
        elif t in alias_map:
            p = alias_map[t]
            if p.id not in extracted:
                extracted[p.id] = ExtractedAttendee(
                    faculty_id=p.id,
                    full_name=p.full_name,
                    initials=p.initials.value,
                    confidence=1.0,
                    match_type="EXACT_ALIAS",
                )

    for p in faculty_profiles:
        if p.id in extracted:
            continue
        sim = fuzz.token_set_ratio(p.full_name.lower(), lower_text)
        if sim >= 85:
            conf = round(sim / 100.0, 2)
            extracted[p.id] = ExtractedAttendee(
                faculty_id=p.id,
                full_name=p.full_name,
                initials=p.initials.value,
                confidence=conf,
                match_type="NAME_FUZZY",
            )

    return list(extracted.values()), False


class CircularExtractor:
    def __init__(
        self,
        doc_confidence_threshold: float = 70.0,
        name_confidence_threshold: float = 0.85,
    ) -> None:
        self._doc_conf_threshold = doc_confidence_threshold
        self._name_conf_threshold = name_confidence_threshold

    def extract(
        self,
        text: str,
        document_confidence: float,
        faculty_profiles: list[FacultyProfile],
        is_probable_duplicate: bool = False,
    ) -> ExtractionResult:
        title, agenda = parse_title_and_agenda(text)
        m_date, date_conf = parse_meeting_date(text)
        m_time = parse_meeting_time(text)
        venue, venue_conf = parse_venue(text)
        attendees, is_all = resolve_circular_attendees(text, faculty_profiles)

        reasons: list[str] = []
        if document_confidence < self._doc_conf_threshold:
            reasons.append("LOW_DOCUMENT_CONFIDENCE")
        if m_date is None or date_conf < 0.85:
            reasons.append("MISSING_OR_UNCERTAIN_DATE")
        if m_time is None or m_time.confidence < 0.85:
            reasons.append("MISSING_OR_UNCERTAIN_TIME")
        if not attendees:
            reasons.append("NO_ATTENDEES_RESOLVED")
        for att in attendees:
            if att.confidence < self._name_conf_threshold:
                reasons.append(f"LOW_CONFIDENCE_ATTENDEE_{att.initials}")
        if is_probable_duplicate:
            reasons.append("PROBABLE_DUPLICATE_EVENT")

        passes_gate = len(reasons) == 0
        return ExtractionResult(
            title=title,
            agenda=agenda,
            meeting_date=m_date,
            date_confidence=date_conf,
            extracted_time=m_time,
            venue=venue,
            venue_confidence=venue_conf,
            attendees=attendees,
            is_all_faculty=is_all,
            review_reasons=reasons,
            is_auto_confirmable=passes_gate,
        )
