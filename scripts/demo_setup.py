import asyncio
import io
import json
import os
import sys
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "samples"
API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8000/api")


def http_post_json(url: str, payload: dict, token: str | None = None, retries: int = 4) -> dict:
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            if err.code == 429 and attempt < retries - 1:
                import time
                time.sleep(4 * (attempt + 1))
                continue
            raise


def http_get_json(url: str, token: str | None = None) -> dict | list:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_post_multipart(url: str, fields: dict, file_field: str, file_path: Path, token: str | None = None) -> dict:
    boundary = "----FacultyDeskFormBoundary" + os.urandom(8).hex()
    body = io.BytesIO()

    for k, v in fields.items():
        body.write(f"--{boundary}\r\n".encode("utf-8"))
        body.write(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode("utf-8"))
        body.write(f"{v}\r\n".encode("utf-8"))

    content_type = "application/octet-stream"
    if file_path.suffix.lower() == ".xlsx":
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif file_path.suffix.lower() == ".pdf":
        content_type = "application/pdf"
    elif file_path.suffix.lower() in (".png", ".jpg", ".jpeg"):
        content_type = f"image/{file_path.suffix.lower().lstrip('.')}"

    body.write(f"--{boundary}\r\n".encode("utf-8"))
    body.write(f'Content-Disposition: form-data; name="{file_field}"; filename="{file_path.name}"\r\n'.encode("utf-8"))
    body.write(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
    body.write(file_path.read_bytes())
    body.write(b"\r\n")
    body.write(f"--{boundary}--\r\n".encode("utf-8"))

    payload = body.getvalue()
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(payload)),
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, data=payload, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def run_demo_setup() -> None:
    print("[*] Setting up FacultyDesk live demonstration environment...")

    print("[1/6] Authenticating HOD and Faculty...")
    hod_auth = http_post_json(f"{API_BASE}/auth/login", {"email": "hod.cse@facultydesk.local", "password": "Hod123!"})
    hod_token = hod_auth["access_token"]
    fac_auth = http_post_json(f"{API_BASE}/auth/login", {"email": "kks@facultydesk.local", "password": "Faculty123!"})
    fac_token = fac_auth["access_token"]

    print("[2/6] Querying active department and terms...")
    depts = http_get_json(f"{API_BASE}/directory/departments", hod_token)
    cse_dept = next(d for d in depts if d["code"] == "CSE")
    dept_id = cse_dept["id"]

    terms = http_get_json(f"{API_BASE}/directory/terms", hod_token)
    term = terms[0] if terms else None
    if not term:
        term = http_post_json(
            f"{API_BASE}/directory/terms",
            {"name": "Fall 2026", "start_date": "2026-08-01", "end_date": "2026-12-31"},
            hod_token,
        )
    term_id = term["id"]

    print("[3/6] Ingesting and confirming sample timetable (standard_timetable.xlsx)...")
    timetable_file = SAMPLES_DIR / "timetables" / "standard_timetable.xlsx"
    upload_res = http_post_multipart(
        f"{API_BASE}/timetables/upload",
        {"academic_term_id": term_id, "department_id": dept_id},
        "file",
        timetable_file,
        hod_token,
    )
    upload_id = upload_res.get("upload_id") or upload_res.get("id")
    for _ in range(10):
        detail = http_get_json(f"{API_BASE}/timetables/{upload_id}", hod_token)
        if detail.get("status") in ("PARSED", "NEEDS_REVIEW"):
            break
        import time; time.sleep(1)

    try:
        http_post_json(f"{API_BASE}/timetables/{upload_id}/confirm", {}, hod_token)
        print("  [✓] Timetable parsed & confirmed, 21-day class recurrence active.")
    except Exception as e:
        print(f"  [!] Note on confirmation: {e}")

    print("[4/6] Processing sample meeting circular (01_clean_text.pdf)...")
    circ_file = SAMPLES_DIR / "circulars" / "01_clean_text.pdf"
    circ_res = http_post_multipart(
        f"{API_BASE}/circulars/upload",
        {"department_id": dept_id},
        "file",
        circ_file,
        fac_token,
    )
    circ_id = circ_res["id"]
    for _ in range(10):
        circ_detail = http_get_json(f"{API_BASE}/circulars/{circ_id}", hod_token)
        if circ_detail.get("status") in ("NEEDS_REVIEW", "CONFIRMED"):
            break
        import time; time.sleep(1)

    try:
        circ_detail = http_get_json(f"{API_BASE}/circulars/{circ_id}", hod_token)
        extracted = circ_detail.get("extracted_fields") or {}
        confirm_payload = {
            "title": extracted.get("title") or "Department Faculty Meeting",
            "meeting_date": extracted.get("date") or "2026-11-05",
            "start_time": extracted.get("start_time") or "14:00:00",
            "end_time": extracted.get("end_time") or "15:00:00",
            "venue": extracted.get("venue") or "Seminar Hall A",
            "attendee_ids": [fac_auth["profile"]["id"]],
        }
        http_post_json(f"{API_BASE}/circulars/{circ_id}/confirm", confirm_payload, hod_token)
        print("  [✓] Circular confirmed and meeting scheduled on attendee calendars.")
    except Exception as e:
        print(f"  [!] Note on circular confirmation: {e}")

    print("[5/6] Scheduling live upcoming meeting (2 minutes ahead with 1-min reminder)...")
    now_utc = datetime.now(UTC)
    meet_start = now_utc + timedelta(minutes=2)
    meet_end = meet_start + timedelta(hours=1)
    try:
        http_post_json(
            f"{API_BASE}/calendar/events",
            {
                "title": "URGENT: Board of Studies Curriculum Review",
                "kind": "MEETING",
                "start_utc": meet_start.isoformat(),
                "end_utc": meet_end.isoformat(),
                "location": "Conference Hall B",
                "attendee_ids": [fac_auth["profile"]["id"]],
                "override_clashes": True,
            },
            hod_token,
        )
        print("  [✓] Upcoming live meeting created; notification scheduled to fire in 1 minute.")
    except Exception as e:
        print(f"  [!] Note on live event creation: {e}")

    print("[6/6] Creating departmental documentation task...")
    task_deadline = now_utc + timedelta(days=2)
    try:
        http_post_json(
            f"{API_BASE}/tasks/assign",
            {
                "title": "NBA Accreditation: Course Outcome Direct Assessment Submission",
                "description": "Upload direct assessment matrix and attainments for Course CS301.",
                "importance": 5,
                "category": "Accreditation",
                "deadline": task_deadline.isoformat(),
                "assignee_ids": [fac_auth["user"]["id"]],
                "department_id": dept_id,
            },
            hod_token,
        )
        print("  [✓] Documentation task created and assigned to faculty.")
    except Exception as e:
        print(f"  [!] Note on task assignment: {e}")

    print("\n" + "=" * 65)
    print("   FACULTYDESK LIVE DEMO ENVIRONMENT READY")
    print("=" * 65)
    print("Web UI:             http://localhost:3000")
    print("Secure HTTPS:       https://localhost (via Caddy)")
    print("API Documentation:  http://localhost:8000/docs")
    print("Mailpit (Emails):   http://localhost:8025")
    print("MinIO Console:      http://localhost:9001 (minioadmin / minioadminpassword)")
    print("-" * 65)
    print("Accounts:")
    print("  • Admin:   admin@facultydesk.local    / Admin123!")
    print("  • HOD:     hod.cse@facultydesk.local  / Hod123!")
    print("  • Faculty: kks@facultydesk.local      / Faculty123!")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    run_demo_setup()
