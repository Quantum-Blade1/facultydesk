from datetime import time
from io import BytesIO
from typing import Any

import openpyxl
from openpyxl.utils import get_column_letter

from app.infrastructure.parsers.cell_tokenizer import tokenize_cell
from app.infrastructure.parsers.header_normalizer import normalize_weekday, parse_time_range
from app.infrastructure.parsers.interfaces import (
    ParsedSlotCandidate,
    ParseResult,
    TimetableParser,
)


class XlsxTimetableParser(TimetableParser):
    def parse(self, content: bytes) -> ParseResult:
        wb = openpyxl.load_workbook(BytesIO(content), data_only=True)
        sheet = wb.active
        if sheet is None:
            return ParseResult(
                unparsed_cells=[{"cell": "A1", "text": "", "reason": "Empty workbook"}]
            )

        merged_lookup: dict[tuple[int, int], tuple[int, int]] = {}
        covered_cells: set[tuple[int, int]] = set()

        for rng in sheet.merged_cells.ranges:
            merged_lookup[(rng.min_row, rng.min_col)] = (rng.max_row, rng.max_col)
            for r in range(rng.min_row, rng.max_row + 1):
                for c in range(rng.min_col, rng.max_col + 1):
                    if (r, c) != (rng.min_row, rng.min_col):
                        covered_cells.add((r, c))

        time_header_row: int | None = None
        col_times: dict[int, tuple[time, time]] = {}

        for r in range(1, min(10, sheet.max_row + 1)):
            detected_times: dict[int, tuple[time, time]] = {}
            for c in range(1, sheet.max_column + 1):
                val = sheet.cell(row=r, column=c).value
                if val:
                    parsed_time = parse_time_range(str(val))
                    if parsed_time:
                        detected_times[c] = parsed_time
            if len(detected_times) >= 2:
                time_header_row = r
                col_times = detected_times
                break

        if time_header_row is None or not col_times:
            return ParseResult(
                unparsed_cells=[
                    {
                        "cell": "HEADER",
                        "text": "",
                        "reason": "Could not detect row with period time ranges",
                    }
                ]
            )

        row_weekdays: dict[int, int] = {}
        for r in range(1, sheet.max_row + 1):
            if r == time_header_row:
                continue
            for c in range(1, min(col_times.keys())):
                val = sheet.cell(row=r, column=c).value
                if val:
                    day_idx = normalize_weekday(str(val))
                    if day_idx is not None:
                        row_weekdays[r] = day_idx
                        break

        candidates: list[ParsedSlotCandidate] = []
        unparsed: list[dict[str, Any]] = []

        for r, weekday in row_weekdays.items():
            for c in sorted(col_times.keys()):
                if (r, c) in covered_cells:
                    continue

                cell = sheet.cell(row=r, column=c)
                val = cell.value
                if not val:
                    continue

                cell_text = str(val).strip()
                if not cell_text:
                    continue

                if (r, c) in merged_lookup:
                    max_r, max_c = merged_lookup[(r, c)]
                    start_t = col_times[c][0]
                    end_c = max_c if max_c in col_times else max(col_times.keys())
                    end_t = col_times[end_c][1]
                    cell_ref = f"{cell.coordinate}:{get_column_letter(max_c)}{max_r}"
                else:
                    start_t = col_times[c][0]
                    end_t = col_times[c][1]
                    cell_ref = cell.coordinate

                tokenized = tokenize_cell(cell_text)
                if not tokenized:
                    unparsed.append(
                        {
                            "cell": cell_ref,
                            "text": cell_text,
                            "reason": "Unrecognized cell format (missing course code or initials)",
                        }
                    )
                    continue

                course_code, section_name, room_code, initials_list = tokenized
                for init in initials_list:
                    candidates.append(
                        ParsedSlotCandidate(
                            weekday=weekday,
                            start_time=start_t,
                            end_time=end_t,
                            course_code=course_code,
                            section_name=section_name,
                            room_code=room_code,
                            raw_initials=[init],
                            source_cell=cell_ref,
                        )
                    )

        return ParseResult(candidates=candidates, unparsed_cells=unparsed)
