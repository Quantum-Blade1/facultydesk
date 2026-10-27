import re

PATTERN_SECTION_INITIALS = re.compile(
    r"^(?P<course>[A-Za-z0-9\s]+?)\s*-\s*(?P<section>[A-Za-z0-9]+)\s*\((?P<initials>[A-Za-z0-9\s/,&]+)\)(?:\s+(?P<room>[A-Za-z0-9\-]+))?$",
    re.IGNORECASE,
)

PATTERN_PAREN_INITIALS = re.compile(
    r"^(?P<course>[A-Za-z0-9\s\-]+?)\s*\((?P<initials>[A-Za-z0-9\s/,&]+)\)(?:\s+(?P<room>[A-Za-z0-9\-]+))?$",
    re.IGNORECASE,
)

PATTERN_SPACE_DELIMITED = re.compile(
    r"^(?P<course>[A-Z]{2,6}[0-9]{0,4})\s+(?P<initials>[A-Z]{2,5})(?:\s+(?P<room>[A-Za-z0-9\-]+))?$",
    re.IGNORECASE,
)

CO_TEACHER_DELIMITERS = re.compile(r"[/,&]")


def split_co_teachers(raw_initials: str) -> list[str]:
    parts = CO_TEACHER_DELIMITERS.split(raw_initials)
    clean: list[str] = []
    for p in parts:
        token = p.strip()
        if token:
            clean.append(token)
    return clean


def tokenize_cell(text: str) -> tuple[str, str | None, str | None, list[str]] | None:
    cleaned = text.strip()
    if not cleaned:
        return None

    match_sec = PATTERN_SECTION_INITIALS.match(cleaned)
    if match_sec:
        course = match_sec.group("course").strip()
        section = match_sec.group("section").strip()
        raw_in = match_sec.group("initials").strip()
        room = match_sec.group("room")
        room_str = room.strip() if room else None
        initials = split_co_teachers(raw_in)
        if initials:
            return course, section, room_str, initials

    match_paren = PATTERN_PAREN_INITIALS.match(cleaned)
    if match_paren:
        course = match_paren.group("course").strip()
        raw_in = match_paren.group("initials").strip()
        room = match_paren.group("room")
        room_str = room.strip() if room else None
        initials = split_co_teachers(raw_in)
        if initials:
            return course, None, room_str, initials

    match_space = PATTERN_SPACE_DELIMITED.match(cleaned)
    if match_space:
        course = match_space.group("course").strip()
        initials_token = match_space.group("initials").strip()
        room = match_space.group("room")
        room_str = room.strip() if room else None
        return course, None, room_str, [initials_token]

    return None
