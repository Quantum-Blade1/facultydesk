from datetime import time
from io import BytesIO
from typing import Any

import pdfplumber

from app.infrastructure.parsers.cell_tokenizer import tokenize_cell
from app.infrastructure.parsers.header_normalizer import normalize_weekday, parse_time_range
from app.infrastructure.parsers.interfaces import (
    ParsedSlotCandidate,
    ParseResult,
    TimetableParser,
)


class PdfTimetableParser(TimetableParser):
    def parse(self, content: bytes) -> ParseResult:
        with pdfplumber.open(BytesIO(content)) as pdf:
            has_any_text = False
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    has_any_text = True
                    break

            if not has_any_text:
                raise ValueError(
                    "Scanned PDF timetables are not supported. "
                    "Please upload an XLSX or CSV timetable."
                )

            candidates: list[ParsedSlotCandidate] = []
            unparsed: list[dict[str, Any]] = []

            for page_idx, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                if not tables:
                    continue

                for tbl_idx, table in enumerate(tables, start=1):
                    if not table or len(table) < 2:
                        continue

                    time_row_idx: int | None = None
                    col_times: dict[int, tuple[time, time]] = {}

                    for r_idx, row in enumerate(table[:5]):
                        detected: dict[int, tuple[time, time]] = {}
                        for c_idx, cell in enumerate(row):
                            if cell:
                                parsed = parse_time_range(cell)
                                if parsed:
                                    detected[c_idx] = parsed
                        if len(detected) >= 2:
                            time_row_idx = r_idx
                            col_times = detected
                            break

                    if time_row_idx is None or not col_times:
                        continue

                    row_weekdays: dict[int, int] = {}
                    min_time_col = min(col_times.keys())
                    for r_idx in range(len(table)):
                        if r_idx == time_row_idx:
                            continue
                        for c_idx in range(min_time_col):
                            cell_val = table[r_idx][c_idx]
                            if cell_val:
                                w = normalize_weekday(cell_val)
                                if w is not None:
                                    row_weekdays[r_idx] = w
                                    break

                    for r_idx, weekday in row_weekdays.items():
                        for c_idx, (t_start, t_end) in col_times.items():
                            if c_idx >= len(table[r_idx]):
                                continue
                            cell_val = table[r_idx][c_idx]
                            if not cell_val or not cell_val.strip():
                                continue

                            cell_text = cell_val.strip()
                            cell_ref = f"P{page_idx}_T{tbl_idx}_R{r_idx + 1}_C{c_idx + 1}"
                            tokenized = tokenize_cell(cell_text)
                            if not tokenized:
                                unparsed.append(
                                    {
                                        "cell": cell_ref,
                                        "text": cell_text,
                                        "reason": (
                                            "Unrecognized cell format "
                                            "(missing course code or initials)"
                                        ),
                                    }
                                )
                                continue

                            course_code, section_name, room_code, initials_list = tokenized
                            for init in initials_list:
                                candidates.append(
                                    ParsedSlotCandidate(
                                        weekday=weekday,
                                        start_time=t_start,
                                        end_time=t_end,
                                        course_code=course_code,
                                        section_name=section_name,
                                        room_code=room_code,
                                        raw_initials=[init],
                                        source_cell=cell_ref,
                                    )
                                )

            if not candidates and not unparsed:
                return ParseResult(
                    unparsed_cells=[
                        {
                            "cell": "PAGE1",
                            "text": "",
                            "reason": (
                                "No tabular timetable structure could be identified in the "
                                "PDF text layer"
                            ),
                        }
                    ]
                )

            return ParseResult(candidates=candidates, unparsed_cells=unparsed)
