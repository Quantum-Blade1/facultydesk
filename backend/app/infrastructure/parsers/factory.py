from app.infrastructure.parsers.csv_parser import CsvTimetableParser
from app.infrastructure.parsers.interfaces import TimetableParser
from app.infrastructure.parsers.pdf_parser import PdfTimetableParser
from app.infrastructure.parsers.xlsx_parser import XlsxTimetableParser


class TimetableParserFactory:
    @staticmethod
    def get_parser(content: bytes, filename: str = "") -> TimetableParser:
        clean_name = filename.lower()
        if content.startswith(b"%PDF") or clean_name.endswith(".pdf"):
            return PdfTimetableParser()

        if content.startswith(b"PK\x03\x04") or clean_name.endswith(".xlsx"):
            return XlsxTimetableParser()

        if clean_name.endswith(".csv"):
            return CsvTimetableParser()

        try:
            content.decode("utf-8")
            return CsvTimetableParser()
        except UnicodeDecodeError:
            pass

        raise ValueError(
            "Unsupported timetable file format. Please upload an .xlsx, .csv, or .pdf file."
        )
