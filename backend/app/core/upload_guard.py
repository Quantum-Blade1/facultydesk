import io
from typing import Final

import pypdfium2
from PIL import Image

from app.core.errors import ValidationError

MAX_UPLOAD_BYTES: Final[int] = 15 * 1024 * 1024
MAX_IMAGE_PIXELS: Final[int] = 25_000_000
MAX_PDF_PAGES: Final[int] = 30

Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS


def detect_mime_and_extension(data: bytes) -> tuple[str, str]:
    if data.startswith(b"%PDF"):
        return "application/pdf", ".pdf"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png", ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg", ".jpg"
    if data.startswith(b"PK\x03\x04"):
        return (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".xlsx",
        )
    try:
        sample = data[:2048].decode("utf-8")
        if "," in sample or ";" in sample or "\t" in sample:
            return "text/csv", ".csv"
    except UnicodeDecodeError:
        pass

    raise ValidationError(
        "File content does not match any allowed format (PDF, PNG, JPEG, XLSX, CSV)"
    )


def validate_upload_content(
    data: bytes,
    allowed_mimes: set[str] | None = None,
) -> tuple[str, str]:
    if not data:
        raise ValidationError("Uploaded file cannot be empty")

    if len(data) > MAX_UPLOAD_BYTES:
        raise ValidationError(f"File size exceeds 15 MB limit: {len(data)} bytes")

    mime, ext = detect_mime_and_extension(data)

    if allowed_mimes is not None and mime not in allowed_mimes:
        raise ValidationError(f"MIME type '{mime}' is not permitted for this operation")

    if mime in ("image/png", "image/jpeg"):
        try:
            with Image.open(io.BytesIO(data)) as img:
                pixels = img.width * img.height
                if pixels > MAX_IMAGE_PIXELS:
                    raise ValidationError(
                        f"Image pixel count {pixels} exceeds decompression limit {MAX_IMAGE_PIXELS}"
                    )
        except Image.DecompressionBombError as e:
            raise ValidationError("Image decompression bomb detected") from e
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Malformed image data: {e}") from e

    elif mime == "application/pdf":
        try:
            pdf = pypdfium2.PdfDocument(data)
            page_count = len(pdf)
            pdf.close()
            if page_count > MAX_PDF_PAGES:
                raise ValidationError(
                    f"PDF page count {page_count} exceeds limit of {MAX_PDF_PAGES} pages"
                )
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Malformed PDF document: {e}") from e

    return mime, ext
