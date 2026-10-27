import io
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def _get_font(size: int = 20) -> Any:
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except Exception:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except Exception:
            return ImageFont.load_default()


def _render_text_to_image(
    lines: list[str],
    width: int = 1200,
    height: int = 1600,
    bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (10, 10, 10),
    draw_table: bool = False,
    table_rows: list[list[str]] | None = None,
) -> Image.Image:
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    font_title = _get_font(28)
    font_body = _get_font(22)
    font_sub = _get_font(20)

    y = 80
    for i, line in enumerate(lines):
        if i == 0 or "Department of Computer Science" in line:
            f = font_title
        elif line.startswith("Subject:") or line.startswith("Sub:"):
            f = font_body
        else:
            f = font_sub

        draw.text((100, y), line, fill=text_color, font=f)
        y += 45

    if draw_table and table_rows:
        y += 20
        col_widths = [100, 450, 200]
        row_height = 45
        start_x = 100

        for _r_idx, row in enumerate(table_rows):
            curr_x = start_x
            for c_idx, cell in enumerate(row):
                w = col_widths[c_idx]
                draw.rectangle(
                    [curr_x, y, curr_x + w, y + row_height],
                    outline=(50, 50, 50),
                    width=2,
                )
                draw.text(
                    (curr_x + 10, y + 10),
                    cell,
                    fill=text_color,
                    font=font_sub,
                )
                curr_x += w
            y += row_height

    return img


def _make_pdf_with_text(lines: list[str]) -> bytes:
    stream_lines = ["BT", "/F1 12 Tf", "50 780 Td", "18 TL"]
    for line in lines:
        safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_lines.append(f"({safe}) '")
    stream_lines.append("ET")
    stream_content = "\n".join(stream_lines).encode("latin-1")

    objects = [
        b"%PDF-1.4\n",
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n",
        f"4 0 obj << /Length {len(stream_content)} >>\nstream\n".encode("latin-1")
        + stream_content
        + b"\nendstream\nendobj\n",
        b"5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
    ]

    out = bytearray()
    offsets = [0]
    for obj in objects:
        if obj.startswith(b"%PDF"):
            out.extend(obj)
            continue
        offsets.append(len(out))
        out.extend(obj)

    xref_offset = len(out)
    out.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode("latin-1"))
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode("latin-1"))

    out.extend(
        f"trailer << /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode(
            "latin-1"
        )
    )
    return bytes(out)


def main() -> None:
    dest_dir = Path("/Users/krishkumarsharma/ai-workspace/projects/facultydesk/samples/circulars")
    dest_dir.mkdir(parents=True, exist_ok=True)

    # 1. Clean PDF with text layer
    c1_lines = [
        "National Institute of Engineering and Technology",
        "Department of Computer Science & Engineering",
        "Ref: CSE/CIR/2026/101",
        "Date: 28/10/2026",
        "",
        "CIRCULAR: CURRICULUM REVIEW MEETING",
        "Subject: Meeting on Curriculum and Syllabus Revision for Term 2",
        "",
        "All designated faculty members are requested to attend a department meeting on",
        "05/11/2026 at 10:30 AM in the Seminar Hall.",
        "",
        "Agenda:",
        "1. Review of syllabus for Semester 4 core subjects.",
        "2. Laboratory manual updates and lab assignment deadlines.",
        "3. Any other matter with permission of the Chair.",
        "",
        "Designated Attendees:",
        "Prof. Krish Sharma (KKS), Dr. Rajesh Sharma (RS), Prof. Priya Nair (PN).",
        "",
        "Sd/-",
        "Head of the Department",
        "Department of Computer Science & Engineering",
    ]
    (dest_dir / "01_clean_text.pdf").write_bytes(_make_pdf_with_text(c1_lines))
    print("Created 01_clean_text.pdf")

    # 2. Scanned PDF (image embedded without text layer)
    c2_lines = [
        "National Institute of Engineering and Technology",
        "Department of Computer Science & Engineering",
        "Ref: CSE/CIR/2026/102",
        "Dated: 29/10/2026",
        "",
        "CIRCULAR: PROJECT EVALUATION COMMITTEE",
        "Subject: Project Evaluation Committee Meeting",
        "",
        "There will be an urgent meeting on 06/11/2026 at 2 pm to 4 pm in Board Room.",
        "",
        "Agenda:",
        "1. Capstone project midterm review.",
        "2. Evaluation rubrics approval.",
        "",
        "Attendees:",
        "Prof. Krish Sharma (KKS), Dr. Rajesh Sharma (RS), Dr. Amit Patel (AP)",
        "",
        "Sd/-",
        "HOD, Computer Science",
    ]
    img2 = _render_text_to_image(c2_lines, bg_color=(250, 250, 248))
    # Convert image to PDF via PIL (pure raster PDF)
    pdf_buf = io.BytesIO()
    img2.save(pdf_buf, format="PDF")
    (dest_dir / "02_scanned.pdf").write_bytes(pdf_buf.getvalue())
    print("Created 02_scanned.pdf")

    # 3. Skewed phone photo (.jpg)
    c3_lines = [
        "National Institute of Engineering and Technology",
        "Department of Computer Science & Engineering",
        "Circular Ref: CSE/CIR/103",
        "Date: 30/10/2026",
        "",
        "CIRCULAR: ACCREDITATION DOCUMENTATION",
        "Subject: Meeting on NBA Accreditation Criteria 4 & 5",
        "",
        "A committee meeting on 08/11/2026 at 1030 hrs in Conference Room.",
        "",
        "Attendees:",
        "Prof. Krish Sharma (KKS), Dr. Manoj Kumar Singh (MKS).",
        "",
        "Head of Department",
    ]
    img3 = _render_text_to_image(c3_lines, bg_color=(245, 245, 240))
    cv_img3 = cv2.cvtColor(np.array(img3), cv2.COLOR_RGB2BGR)
    h, w = cv_img3.shape[:2]
    # Rotate by 3.8 degrees
    M = cv2.getRotationMatrix2D((w / 2, h / 2), 3.8, 1.0)
    skewed_cv3 = cv2.warpAffine(
        cv_img3, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(240, 240, 235)
    )
    cv2.imwrite(str(dest_dir / "03_skewed_phone.jpg"), skewed_cv3)
    print("Created 03_skewed_phone.jpg")

    # 4. Low light phone photo (.jpg)
    c4_lines = [
        "National Institute of Engineering and Technology",
        "Department of Computer Science & Engineering",
        "Circular: CSE/2026/104",
        "Date: 31/10/2026",
        "",
        "CIRCULAR: INTERNAL ASSESSMENT MARKS",
        "Subject: Internal Assessment Marks Moderation Meeting",
        "",
        "A meeting on 10/11/2026 at 10.30 am in Room 301.",
        "",
        "Attendees:",
        "Prof. Krish Sharma (KKS), Prof. Priya Nair (PN)",
        "",
        "Sd/-",
        "HOD",
    ]
    img4 = _render_text_to_image(c4_lines, bg_color=(240, 240, 240))
    cv_img4 = cv2.cvtColor(np.array(img4), cv2.COLOR_RGB2BGR)
    # Low light transform: multiply by 0.38 and add noise
    low_light = (cv_img4.astype(np.float32) * 0.38).astype(np.uint8)
    noise = np.random.normal(0, 10, low_light.shape).astype(np.int16)
    noisy = np.clip(low_light.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    cv2.imwrite(str(dest_dir / "04_low_light.jpg"), noisy)
    print("Created 04_low_light.jpg")

    # 5. Table initials (.png)
    c5_lines = [
        "National Institute of Engineering and Technology",
        "Department of Computer Science & Engineering",
        "Circular No: CSE/2026/105",
        "Date: 01/11/2026",
        "",
        "CIRCULAR: LAB SAFETY AND AUDIT",
        "Subject: Lab Safety and Audit Committee Meeting",
        "",
        "The committee meeting will be held on 12/11/2026 at 14:00-15:30 in Computer Center Lab 1.",
        "",
        "The following faculty members are required to attend:",
    ]
    c5_table = [
        ["S.No", "Faculty Name", "Initials"],
        ["1", "Prof. Krish Sharma", "KKS"],
        ["2", "Dr. Rajesh Sharma", "RS"],
        ["3", "Prof. Priya Nair", "PN"],
    ]
    img5 = _render_text_to_image(
        c5_lines,
        bg_color=(255, 255, 255),
        draw_table=True,
        table_rows=c5_table,
    )
    img5.save(dest_dir / "05_table_initials.png")
    print("Created 05_table_initials.png")

    # 6. All faculty circular (.pdf)
    c6_lines = [
        "National Institute of Engineering and Technology",
        "Department of Computer Science & Engineering",
        "Circular Ref: CSE/2026/106",
        "Date: 01/11/2026",
        "",
        "CIRCULAR: DEPARTMENT GENERAL BODY MEETING",
        "Subject: General Body Meeting on Academic Term Review",
        "",
        "All faculty members of the Department of Computer Science are requested to",
        "attend the meeting scheduled on 15/11/2026 at 3:00 PM in the Auditorium.",
        "",
        "Agenda:",
        "1. Academic progress review and student attendance.",
        "2. Research grant application submissions.",
        "3. Feedback collection timeline.",
        "",
        "Sd/-",
        "Head of the Department",
    ]
    (dest_dir / "06_all_faculty.pdf").write_bytes(_make_pdf_with_text(c6_lines))
    print("Created 06_all_faculty.pdf")
    print("\nAll 6 synthetic circular samples generated successfully.")


if __name__ == "__main__":
    main()
