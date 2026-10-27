import csv
import io
from dataclasses import dataclass, field
from uuid import UUID, uuid4

from openpyxl import load_workbook

from app.application.security.policy import AuthorisationPolicy, Principal
from app.core.clock import Clock
from app.core.security import hash_password
from app.domain import (
    AuditLog,
    FacultyProfile,
    Initials,
    InvariantViolation,
    Role,
    UnitOfWork,
    User,
)


@dataclass(frozen=True)
class RowImportResult:
    row_number: int
    status: str
    message: str
    email: str | None = None
    initials: str | None = None


@dataclass
class BulkImportReport:
    total_rows: int = 0
    created_count: int = 0
    updated_count: int = 0
    rejected_count: int = 0
    rows: list[RowImportResult] = field(default_factory=list)


class BulkImportFacultyUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        principal: Principal,
        department_id: UUID,
        file_content: bytes,
        file_extension: str,
    ) -> BulkImportReport:
        AuthorisationPolicy.enforce(
            principal, resource_dept_id=department_id, action="bulk_import_faculty"
        )

        rows_data = self._parse_file(file_content, file_extension)
        report = BulkImportReport(total_rows=len(rows_data))

        seen_initials_in_batch: set[str] = set()

        async with self._uow:
            dept = await self._uow.departments.get_by_id(department_id)
            if dept is None:
                raise ValueError(f"Department {department_id} does not exist")

            for row_idx, raw_row in enumerate(rows_data, start=2):
                full_name = raw_row.get("full_name", "").strip()
                initials_raw = raw_row.get("initials", "").strip()
                email = raw_row.get("email", "").strip().lower()
                aliases_raw = raw_row.get("aliases", "").strip()
                aliases = tuple(a.strip() for a in aliases_raw.split(";") if a.strip())

                if not full_name or not initials_raw or not email:
                    report.rejected_count += 1
                    report.rows.append(
                        RowImportResult(
                            row_number=row_idx,
                            status="REJECTED",
                            message="Missing required field(s): full_name, initials, or email",
                            email=email or None,
                            initials=initials_raw or None,
                        )
                    )
                    continue

                if "@" not in email or "." not in email.split("@")[-1]:
                    report.rejected_count += 1
                    report.rows.append(
                        RowImportResult(
                            row_number=row_idx,
                            status="REJECTED",
                            message=f"Invalid email format: '{email}'",
                            email=email,
                            initials=initials_raw,
                        )
                    )
                    continue

                try:
                    initials = Initials(initials_raw)
                except InvariantViolation as e:
                    report.rejected_count += 1
                    report.rows.append(
                        RowImportResult(
                            row_number=row_idx,
                            status="REJECTED",
                            message=str(e),
                            email=email,
                            initials=initials_raw,
                        )
                    )
                    continue

                if initials.value in seen_initials_in_batch:
                    report.rejected_count += 1
                    report.rows.append(
                        RowImportResult(
                            row_number=row_idx,
                            status="REJECTED",
                            message=f"Duplicate initials '{initials.value}' in import batch",
                            email=email,
                            initials=initials.value,
                        )
                    )
                    continue

                existing_by_init = (
                    await self._uow.faculty_profiles.get_by_department_and_initials(
                        department_id, initials
                    )
                )
                existing_user = await self._uow.users.get_by_email(email)

                if existing_by_init is not None and (
                    existing_user is None or existing_by_init.user_id != existing_user.id
                ):
                    report.rejected_count += 1
                    msg = (
                        f"Initials '{initials.value}' are already taken by another "
                        f"faculty member in this department"
                    )
                    report.rows.append(
                        RowImportResult(
                            row_number=row_idx,
                            status="REJECTED",
                            message=msg,
                            email=email,
                            initials=initials.value,
                        )
                    )
                    continue

                seen_initials_in_batch.add(initials.value)

                if existing_user is not None:
                    profile = await self._uow.faculty_profiles.get_by_user_id(existing_user.id)
                    if profile is not None:
                        profile.full_name = full_name
                        profile.initials = initials
                        profile.aliases = aliases
                        profile.department_id = department_id
                        await self._uow.faculty_profiles.save(profile)
                        report.updated_count += 1
                        report.rows.append(
                            RowImportResult(
                                row_number=row_idx,
                                status="UPDATED",
                                message="Faculty profile updated",
                                email=email,
                                initials=initials.value,
                            )
                        )
                        continue

                new_user = User(
                    id=uuid4(),
                    email=email,
                    password_hash=hash_password("FacultyDesk123!"),
                    role=Role.FACULTY,
                    is_active=True,
                )
                await self._uow.users.save(new_user)

                new_profile = FacultyProfile(
                    id=uuid4(),
                    user_id=new_user.id,
                    department_id=department_id,
                    full_name=full_name,
                    initials=initials,
                    aliases=aliases,
                    email=email,
                )
                await self._uow.faculty_profiles.save(new_profile)
                report.created_count += 1
                report.rows.append(
                    RowImportResult(
                        row_number=row_idx,
                        status="CREATED",
                        message="Faculty profile created",
                        email=email,
                        initials=initials.value,
                    )
                )

            audit = AuditLog(
                user_id=principal.user_id,
                action="BULK_IMPORT_FACULTY",
                resource_type="Department",
                resource_id=str(department_id),
                payload={
                    "total": report.total_rows,
                    "created": report.created_count,
                    "updated": report.updated_count,
                    "rejected": report.rejected_count,
                },
                timestamp_utc=self._clock.now(),
            )
            await self._uow.audit_logs.save(audit)
            await self._uow.commit()

        return report

    def _parse_file(
        self, file_content: bytes, file_extension: str
    ) -> list[dict[str, str]]:
        ext = file_extension.lower().lstrip(".")
        if ext == "csv":
            text = file_content.decode("utf-8-sig", errors="replace")
            reader = csv.DictReader(io.StringIO(text))
            rows: list[dict[str, str]] = []
            if reader.fieldnames:
                normalized_fields = {fn.strip().lower(): fn for fn in reader.fieldnames}
                for r in reader:
                    rows.append(
                        {
                            "full_name": r.get(normalized_fields.get("full_name", ""), ""),
                            "initials": r.get(normalized_fields.get("initials", ""), ""),
                            "email": r.get(normalized_fields.get("email", ""), ""),
                            "aliases": r.get(normalized_fields.get("aliases", ""), ""),
                        }
                    )
            return rows

        if ext in ("xlsx", "xls"):
            wb = load_workbook(filename=io.BytesIO(file_content), data_only=True)
            sheet = wb.active
            if sheet is None:
                return []
            header_map: dict[str, int] = {}
            for col_idx, cell in enumerate(sheet[1], start=1):
                if cell.value:
                    header_map[str(cell.value).strip().lower()] = col_idx

            rows = []
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not any(row):
                    continue
                fn_idx = header_map.get("full_name")
                in_idx = header_map.get("initials")
                em_idx = header_map.get("email")
                al_idx = header_map.get("aliases")

                full_name = str(row[fn_idx - 1]) if fn_idx and row[fn_idx - 1] is not None else ""
                initials = str(row[in_idx - 1]) if in_idx and row[in_idx - 1] is not None else ""
                email = str(row[em_idx - 1]) if em_idx and row[em_idx - 1] is not None else ""
                aliases = str(row[al_idx - 1]) if al_idx and row[al_idx - 1] is not None else ""

                rows.append(
                    {
                        "full_name": full_name,
                        "initials": initials,
                        "email": email,
                        "aliases": aliases,
                    }
                )
            return rows

        raise ValueError(f"Unsupported file extension: {file_extension}")
