import io
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import pytest
from PIL import Image

from app.api.routers.metrics import compute_lateness_percentiles
from app.core.errors import ValidationError
from app.core.upload_guard import (
    MAX_UPLOAD_BYTES,
    detect_mime_and_extension,
    validate_upload_content,
)
from app.infrastructure.storage.backup_service import BACKUP_BUCKET, BackupService


def test_detect_mime_and_extension_valid() -> None:
    pdf_bytes = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\nstartxref\n0\n%%EOF"
    mime, ext = detect_mime_and_extension(pdf_bytes)
    assert mime == "application/pdf"
    assert ext == ".pdf"

    png_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"
    )
    mime, ext = detect_mime_and_extension(png_bytes)
    assert mime == "image/png"
    assert ext == ".png"

    jpeg_bytes = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    mime, ext = detect_mime_and_extension(jpeg_bytes)
    assert mime == "image/jpeg"
    assert ext == ".jpg"

    zip_bytes = b"PK\x03\x04\x14\x00\x00\x00\x08\x00"
    mime, ext = detect_mime_and_extension(zip_bytes)
    assert mime == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert ext == ".xlsx"

    csv_bytes = b"code,name,initials\nCS101,Data Structures,DS\n"
    mime, ext = detect_mime_and_extension(csv_bytes)
    assert mime == "text/csv"
    assert ext == ".csv"


def test_detect_mime_and_extension_invalid() -> None:
    garbage = b"\x00\x01\x02\x03\x04\x05\x06\x07"
    with pytest.raises(ValidationError):
        detect_mime_and_extension(garbage)


def test_validate_upload_content_size_limit() -> None:
    oversized = b"%PDF-1.4\n" + b"A" * (MAX_UPLOAD_BYTES + 10)
    with pytest.raises(ValidationError, match="File size exceeds 15 MB limit"):
        validate_upload_content(oversized, allowed_mimes={"application/pdf"})


def test_validate_upload_content_mime_disallowed() -> None:
    csv_bytes = b"header1,header2\n1,2\n"
    with pytest.raises(ValidationError, match="is not permitted for this operation"):
        validate_upload_content(csv_bytes, allowed_mimes={"application/pdf"})


def test_validate_upload_content_image_decompression_guard() -> None:
    buf = io.BytesIO()
    img = Image.new("RGB", (6000, 5000), color="white")
    img.save(buf, format="PNG")
    huge_image_bytes = buf.getvalue()

    with pytest.raises(ValidationError, match="exceeds decompression limit"):
        validate_upload_content(huge_image_bytes, allowed_mimes={"image/png"})


def test_compute_lateness_percentiles_empty() -> None:
    pcts = compute_lateness_percentiles([])
    assert pcts["p50"] == 0.0
    assert pcts["p95"] == 0.0
    assert pcts["p99"] == 0.0


def test_compute_lateness_percentiles_single() -> None:
    pcts = compute_lateness_percentiles([42.5])
    assert pcts["p50"] == 42.5
    assert pcts["p95"] == 42.5
    assert pcts["p99"] == 42.5


def test_compute_lateness_percentiles_100_elements() -> None:
    data = [float(i) for i in range(1, 101)]
    pcts = compute_lateness_percentiles(data)
    assert abs(pcts["p50"] - 50.5) < 1e-4
    assert abs(pcts["p95"] - 95.05) < 1e-4
    assert abs(pcts["p99"] - 99.01) < 1e-4


def test_backup_prune_expired() -> None:
    mock_minio = MagicMock()
    now_utc = datetime.now(UTC)

    obj_recent = MagicMock()
    obj_recent.object_name = "facultydesk_backup_20261027_100000.sql.gz"
    obj_recent.last_modified = now_utc - timedelta(days=2)

    obj_expired1 = MagicMock()
    obj_expired1.object_name = "facultydesk_backup_20261001_100000.sql.gz"
    obj_expired1.last_modified = now_utc - timedelta(days=20)

    obj_expired2 = MagicMock()
    obj_expired2.object_name = "facultydesk_backup_20261005_100000.sql.gz"
    obj_expired2.last_modified = now_utc - timedelta(days=16)

    mock_minio.bucket_exists.return_value = True
    mock_minio.list_objects.return_value = [obj_recent, obj_expired1, obj_expired2]

    service = BackupService(client=mock_minio)
    pruned = service.prune_expired_backups()

    assert pruned == 2
    mock_minio.remove_object.assert_any_call(
        BACKUP_BUCKET, "facultydesk_backup_20261001_100000.sql.gz"
    )
    mock_minio.remove_object.assert_any_call(
        BACKUP_BUCKET, "facultydesk_backup_20261005_100000.sql.gz"
    )


def test_backup_prune_preserves_single_expired_backup() -> None:
    mock_minio = MagicMock()
    now_utc = datetime.now(UTC)

    only_obj = MagicMock()
    only_obj.object_name = "facultydesk_backup_20260901_100000.sql.gz"
    only_obj.last_modified = now_utc - timedelta(days=50)

    mock_minio.bucket_exists.return_value = True
    mock_minio.list_objects.return_value = [only_obj]

    service = BackupService(client=mock_minio)
    pruned = service.prune_expired_backups()

    assert pruned == 0
    mock_minio.remove_object.assert_not_called()
