import io

import cv2
import numpy as np
import pdfplumber
import pypdfium2


def has_pdf_text_layer(pdf_bytes: bytes) -> tuple[bool, str]:
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            extracted_pages: list[str] = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_pages.append(text.strip())
            full_text = "\n\n".join(extracted_pages).strip()
            if len(full_text) >= 30:
                return True, full_text
            return False, ""
    except Exception:
        return False, ""


def rasterise_pdf_page(pdf_bytes: bytes, page_index: int = 0, dpi: int = 300) -> bytes:
    pdf = pypdfium2.PdfDocument(pdf_bytes)
    if page_index >= len(pdf):
        page_index = 0
    page = pdf[page_index]
    scale = dpi / 72.0
    bitmap = page.render(scale=scale)
    pil_image = bitmap.to_pil()
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    return buf.getvalue()


def compute_deskew_angle(binary_image: np.ndarray) -> float:
    coords = cv2.findNonZero(binary_image)
    if coords is None or len(coords) < 100:
        return 0.0

    rect = cv2.minAreaRect(coords)
    phi = rect[2]
    if phi < -45.0:
        angle = phi + 90.0
    elif phi > 45.0:
        angle = phi - 90.0
    else:
        angle = phi

    if abs(angle) < 0.5:
        return 0.0
    return float(angle)


def deskew_image(image: np.ndarray, angle: float) -> np.ndarray:
    if abs(angle) < 0.5:
        return image
    h, w = image.shape[:2]
    center = (w / 2.0, h / 2.0)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(
        image,
        matrix,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )


def preprocess_image_for_ocr(image_bytes: bytes) -> tuple[np.ndarray, float]:
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to decode image from provided bytes")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    thresh = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        21,
        10,
    )

    angle = compute_deskew_angle(thresh)
    if abs(angle) >= 0.5:
        denoised = deskew_image(denoised, angle)

    return denoised, angle
