from app.infrastructure.ocr.duplicate_detector import detect_probable_duplicate
from app.infrastructure.ocr.engine import (
    OcrEngine,
    OcrResult,
    WordBox,
    compute_length_weighted_confidence,
)
from app.infrastructure.ocr.extractor import (
    CircularExtractor,
    ExtractedAttendee,
    ExtractedTime,
    ExtractionResult,
    parse_meeting_date,
    parse_meeting_time,
    parse_venue,
)
from app.infrastructure.ocr.preprocessor import (
    compute_deskew_angle,
    deskew_image,
    has_pdf_text_layer,
    preprocess_image_for_ocr,
    rasterise_pdf_page,
)

__all__ = [
    "CircularExtractor",
    "ExtractedAttendee",
    "ExtractedTime",
    "ExtractionResult",
    "OcrEngine",
    "OcrResult",
    "WordBox",
    "compute_deskew_angle",
    "compute_length_weighted_confidence",
    "deskew_image",
    "detect_probable_duplicate",
    "has_pdf_text_layer",
    "parse_meeting_date",
    "parse_meeting_time",
    "parse_venue",
    "preprocess_image_for_ocr",
    "rasterise_pdf_page",
]
