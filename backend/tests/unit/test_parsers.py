from datetime import time
from pathlib import Path

import pytest

from app.infrastructure.parsers.factory import TimetableParserFactory
from app.infrastructure.parsers.pdf_parser import PdfTimetableParser

SAMPLES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "samples" / "timetables"


def test_xlsx_standard_timetable_parsing() -> None:
    path = SAMPLES_DIR / "standard_timetable.xlsx"
    content = path.read_bytes()
    parser = TimetableParserFactory.get_parser(content, path.name)
    result = parser.parse(content)

    assert len(result.candidates) == 9
    assert len(result.unparsed_cells) == 0

    c0 = result.candidates[0]
    assert c0.weekday == 1
    assert c0.start_time == time(9, 0)
    assert c0.end_time == time(9, 55)
    assert c0.course_code == "CN"
    assert c0.raw_initials == ["KKS"]


def test_xlsx_merged_cell_period_expansion() -> None:
    path = SAMPLES_DIR / "merged_labs_timetable.xlsx"
    content = path.read_bytes()
    parser = TimetableParserFactory.get_parser(content, path.name)
    result = parser.parse(content)

    assert len(result.candidates) >= 3

    merged_slot = next(c for c in result.candidates if c.course_code == "DBMS Lab")
    assert merged_slot.weekday == 1
    assert merged_slot.start_time == time(10, 0)
    assert merged_slot.end_time == time(11, 55)
    assert merged_slot.section_name == "A1"
    assert merged_slot.room_code == "LAB-1"
    assert merged_slot.raw_initials == ["RS"]


def test_xlsx_co_teachers_parsing() -> None:
    path = SAMPLES_DIR / "co_teachers_timetable.xlsx"
    content = path.read_bytes()
    parser = TimetableParserFactory.get_parser(content, path.name)
    result = parser.parse(content)

    dbms_slots = [c for c in result.candidates if c.course_code == "DBMS Lab"]
    assert len(dbms_slots) == 2
    assert {s.raw_initials[0] for s in dbms_slots} == {"RS", "PN"}

    se_slots = [c for c in result.candidates if c.course_code == "SE"]
    assert len(se_slots) == 2
    assert {s.raw_initials[0] for s in se_slots} == {"AP", "MKS"}


def test_csv_timetable_parsing() -> None:
    path = SAMPLES_DIR / "timetable.csv"
    content = path.read_bytes()
    parser = TimetableParserFactory.get_parser(content, path.name)
    result = parser.parse(content)

    assert len(result.candidates) == 6
    assert len(result.unparsed_cells) == 0

    c0 = result.candidates[0]
    assert c0.weekday == 1
    assert c0.start_time == time(9, 0)
    assert c0.end_time == time(9, 55)
    assert c0.course_code == "CN"
    assert c0.section_name == "A"
    assert c0.room_code == "301"
    assert c0.raw_initials == ["KKS"]


def test_pdf_text_timetable_parsing() -> None:
    path = SAMPLES_DIR / "text_timetable.pdf"
    content = path.read_bytes()
    parser = TimetableParserFactory.get_parser(content, path.name)
    result = parser.parse(content)

    assert len(result.candidates) >= 4
    c0 = result.candidates[0]
    assert c0.weekday == 1
    assert c0.start_time == time(9, 0)
    assert c0.end_time == time(9, 55)
    assert c0.course_code == "CN"
    assert c0.raw_initials == ["KKS"]


def test_scanned_pdf_rejection() -> None:
    empty_pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >> endobj\n"
        b"xref\n0 4\n0000000000 65535 f \n"
        b"0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n"
        b"trailer << /Size 4 /Root 1 0 R >>\nstartxref\n185\n%%EOF"
    )
    parser = PdfTimetableParser()
    with pytest.raises(ValueError, match="Scanned PDF timetables are not supported"):
        parser.parse(empty_pdf)
