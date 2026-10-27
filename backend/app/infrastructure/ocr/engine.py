from dataclasses import dataclass
from typing import Any

import numpy as np
import pytesseract


@dataclass(frozen=True)
class WordBox:
    text: str
    confidence: float
    left: int
    top: int
    width: int
    height: int


@dataclass(frozen=True)
class OcrResult:
    text: str
    confidence: float
    word_boxes: list[WordBox]
    psm_used: int


def compute_length_weighted_confidence(words: list[str], confidences: list[float]) -> float:
    weighted_sum = 0.0
    total_len = 0

    for w, c in zip(words, confidences, strict=False):
        cleaned = w.strip()
        if c >= 0.0 and len(cleaned) > 0:
            word_len = len(cleaned)
            weighted_sum += word_len * c
            total_len += word_len

    if total_len == 0:
        return 0.0
    return round(weighted_sum / total_len, 2)


class OcrEngine:
    def __init__(self, confidence_threshold: float = 70.0) -> None:
        self._confidence_threshold = confidence_threshold

    def _execute_psm(self, image: np.ndarray, psm: int) -> OcrResult:
        config = f"--oem 1 --psm {psm}"
        data: dict[str, list[Any]] = pytesseract.image_to_data(
            image, output_type=pytesseract.Output.DICT, config=config
        )

        raw_texts: list[str] = [str(t) for t in data.get("text", [])]
        raw_confs: list[float] = [float(c) for c in data.get("conf", [])]
        lefts: list[int] = [int(v) for v in data.get("left", [])]
        tops: list[int] = [int(v) for v in data.get("top", [])]
        widths: list[int] = [int(v) for v in data.get("width", [])]
        heights: list[int] = [int(v) for v in data.get("height", [])]

        boxes: list[WordBox] = []
        assembled_lines: list[str] = []
        current_line: list[str] = []
        prev_line_num: int = -1
        line_nums: list[int] = [int(v) for v in data.get("line_num", [])]

        for i, text in enumerate(raw_texts):
            clean = text.strip()
            conf = raw_confs[i]
            if not clean:
                continue

            ln = line_nums[i] if i < len(line_nums) else 0
            if prev_line_num != -1 and ln != prev_line_num and current_line:
                assembled_lines.append(" ".join(current_line))
                current_line = []
            prev_line_num = ln
            current_line.append(clean)

            if conf >= 0.0:
                boxes.append(
                    WordBox(
                        text=clean,
                        confidence=conf,
                        left=lefts[i] if i < len(lefts) else 0,
                        top=tops[i] if i < len(tops) else 0,
                        width=widths[i] if i < len(widths) else 0,
                        height=heights[i] if i < len(heights) else 0,
                    )
                )

        if current_line:
            assembled_lines.append(" ".join(current_line))

        full_text = "\n".join(assembled_lines).strip()
        doc_conf = compute_length_weighted_confidence(
            [b.text for b in boxes], [b.confidence for b in boxes]
        )

        return OcrResult(
            text=full_text,
            confidence=doc_conf,
            word_boxes=boxes,
            psm_used=psm,
        )

    def extract_text(self, image: np.ndarray) -> OcrResult:
        res_psm6 = self._execute_psm(image, psm=6)
        res_psm4 = self._execute_psm(image, psm=4)

        if len(res_psm4.word_boxes) > len(res_psm6.word_boxes) + 5 and res_psm4.confidence >= 70.0:
            return res_psm4

        if (
            res_psm6.confidence < self._confidence_threshold
            and res_psm4.confidence > res_psm6.confidence
        ):
            return res_psm4

        return res_psm6
