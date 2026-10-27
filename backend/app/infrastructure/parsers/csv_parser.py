import csv
from datetime import time
from io import StringIO
from typing import Any

from app.infrastructure.parsers.cell_tokenizer import split_co_teachers
from app.infrastructure.parsers.header_normalizer import normalize_weekday
from app.infrastructure.parsers.interfaces import (
    ParsedSlotCandidate,
    ParseResult,
    TimetableParser,
)


def _parse_clock_time(val: str) -> time | None:
    cleaned = val.strip().lower()
    for sep in [":", "."]:
        if sep in cleaned:
            parts = cleaned.split(sep)
            if len(parts) == 2:
                try:
                    h, m = int(parts[0]), int(parts[1])
                    if 0 <= h < 24 and 0 <= m < 60:
                        return time(h, m)
                except ValueError:
                    return None
    return None


def _get_col(row: list[str], indices: dict[str, int], name: str) -> str:
    idx = indices.get(name)
    if idx is not None and idx < len(row):
        return row[idx].strip()
    return ""


class CsvTimetableParser(TimetableParser):
    def parse(self, content: bytes) -> ParseResult:
        text = content.decode("utf-8-sig", errors="replace")
        reader = csv.reader(StringIO(text))
        candidates: list[ParsedSlotCandidate] = []
        unparsed: list[dict[str, Any]] = []

        rows = [row for row in reader if row and any(c.strip() for c in row)]
        if not rows:
            return ParseResult(
                unparsed_cells=[{"cell": "ROW1", "text": "", "reason": "Empty CSV file"}]
            )

        header = [c.strip().lower() for c in rows[0]]
        has_header = False
        col_indices: dict[str, int] = {}

        if any(h in ["day", "course", "initials", "start"] for h in header):
            has_header = True
            for idx, h in enumerate(header):
                col_indices[h] = idx

        start_row_idx = 1 if has_header else 0

        for row_num, row in enumerate(rows[start_row_idx:], start=start_row_idx + 1):
            if len(row) < 4:
                unparsed.append(
                    {
                        "cell": f"ROW{row_num}",
                        "text": ",".join(row),
                        "reason": (
                            "Insufficient columns "
                            "(expected at least day, start, end, course, initials)"
                        ),
                    }
                )
                continue

            if has_header:
                day_val = _get_col(row, col_indices, "day")
                start_val = _get_col(row, col_indices, "start")
                end_val = _get_col(row, col_indices, "end")
                course_val = _get_col(row, col_indices, "course")
                sec_raw = _get_col(row, col_indices, "section")
                room_raw = _get_col(row, col_indices, "room")
                init_val = _get_col(row, col_indices, "initials")
                sec_val = sec_raw if sec_raw else None
                room_val = room_raw if room_raw else None
            else:
                day_val = row[0]
                start_val = row[1]
                end_val = row[2]
                course_val = row[3]
                sec_val = row[4].strip() if len(row) > 4 and row[4].strip() else None
                room_val = row[5].strip() if len(row) > 5 and row[5].strip() else None
                init_val = row[6] if len(row) > 6 else ""

            weekday = normalize_weekday(day_val)
            if weekday is None:
                try:
                    day_int = int(day_val.strip())
                    if 1 <= day_int <= 7:
                        weekday = day_int
                except ValueError:
                    pass

            if weekday is None:
                unparsed.append(
                    {
                        "cell": f"ROW{row_num}:COL1",
                        "text": day_val,
                        "reason": f"Invalid day representation '{day_val}'",
                    }
                )
                continue

            t_start = _parse_clock_time(start_val)
            t_end = _parse_clock_time(end_val)
            if not t_start or not t_end:
                unparsed.append(
                    {
                        "cell": f"ROW{row_num}:TIME",
                        "text": f"{start_val}-{end_val}",
                        "reason": "Invalid start or end time format",
                    }
                )
                continue

            course_code = course_val.strip()
            if not course_code:
                unparsed.append(
                    {
                        "cell": f"ROW{row_num}:COURSE",
                        "text": "",
                        "reason": "Course code cannot be empty",
                    }
                )
                continue

            initials = split_co_teachers(init_val)
            if not initials:
                unparsed.append(
                    {
                        "cell": f"ROW{row_num}:INITIALS",
                        "text": init_val,
                        "reason": "No faculty initials provided",
                    }
                )
                continue

            section_clean = sec_val.strip() if sec_val and sec_val.strip() else None
            room_clean = room_val.strip() if room_val and room_val.strip() else None

            for init in initials:
                candidates.append(
                    ParsedSlotCandidate(
                        weekday=weekday,
                        start_time=t_start,
                        end_time=t_end,
                        course_code=course_code,
                        section_name=section_clean,
                        room_code=room_clean,
                        raw_initials=[init],
                        source_cell=f"ROW{row_num}",
                    )
                )

        return ParseResult(candidates=candidates, unparsed_cells=unparsed)
