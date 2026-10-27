from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from pydantic import BaseModel

from app.api.deps import (
    get_clock,
    get_current_principal,
    get_uow,
    require_admin,
    require_hod_or_admin,
)
from app.application.directory.bulk_import import BulkImportFacultyUseCase
from app.application.directory.create_faculty import CreateFacultyUseCase
from app.application.directory.deactivate_faculty import DeactivateFacultyUseCase
from app.application.directory.terms import ManageTermsUseCase
from app.application.directory.update_faculty import UpdateFacultyUseCase
from app.application.security.policy import Principal
from app.core.clock import Clock
from app.core.errors import NotFoundError, ValidationError
from app.domain import UnitOfWork

router = APIRouter(prefix="/directory", tags=["directory"])


class DepartmentResponse(BaseModel):
    id: UUID
    code: str
    name: str


class FacultyProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    department_id: UUID
    full_name: str
    initials: str
    aliases: list[str]
    email: str
    phone: str | None


class CreateFacultyRequest(BaseModel):
    department_id: UUID
    full_name: str
    initials: str
    email: str
    aliases: list[str] = []
    phone: str | None = None
    initial_password: str = "FacultyDesk123!"


class UpdateFacultyRequest(BaseModel):
    full_name: str | None = None
    initials: str | None = None
    aliases: list[str] | None = None
    phone: str | None = None


class AcademicTermResponse(BaseModel):
    id: UUID
    name: str
    start_date: date
    end_date: date
    timezone: str


class CreateAcademicTermRequest(BaseModel):
    name: str
    start_date: date
    end_date: date
    timezone: str = "Asia/Kolkata"


class HolidayResponse(BaseModel):
    id: UUID
    academic_term_id: UUID
    date: date
    label: str


class CreateHolidayRequest(BaseModel):
    date: date
    label: str


class RowImportResultResponse(BaseModel):
    row_number: int
    status: str
    message: str
    email: str | None
    initials: str | None


class BulkImportResponse(BaseModel):
    total_rows: int
    created_count: int
    updated_count: int
    rejected_count: int
    rows: list[RowImportResultResponse]


class StatusResponse(BaseModel):
    status: str


@router.get("/departments", response_model=list[DepartmentResponse])
async def list_departments(
    uow: UnitOfWork = Depends(get_uow),
) -> list[DepartmentResponse]:
    """List all registered academic departments."""
    async with uow:
        depts = await uow.departments.list_all()
    return [DepartmentResponse(id=d.id, code=d.code, name=d.name) for d in depts]


@router.get(
    "/departments/{department_id}/faculty",
    response_model=list[FacultyProfileResponse],
)
async def list_department_faculty(
    department_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
) -> list[FacultyProfileResponse]:
    """List faculty members belonging to a department."""
    async with uow:
        profiles = await uow.faculty_profiles.list_by_department(department_id)
    return [
        FacultyProfileResponse(
            id=p.id,
            user_id=p.user_id,
            department_id=p.department_id,
            full_name=p.full_name,
            initials=p.initials.value,
            aliases=list(p.aliases),
            email=p.email,
            phone=p.phone,
        )
        for p in profiles
    ]


@router.get("/faculty", response_model=list[FacultyProfileResponse])
async def list_faculty(
    department_id: UUID | None = None,
    uow: UnitOfWork = Depends(get_uow),
) -> list[FacultyProfileResponse]:
    """List faculty profiles across the department or institution."""
    async with uow:
        if department_id is not None:
            profiles = await uow.faculty_profiles.list_by_department(department_id)
        else:
            profiles = await uow.faculty_profiles.list_all()
    return [
        FacultyProfileResponse(
            id=p.id,
            user_id=p.user_id,
            department_id=p.department_id,
            full_name=p.full_name,
            initials=p.initials.value,
            aliases=list(p.aliases),
            email=p.email,
            phone=p.phone,
        )
        for p in profiles
    ]


@router.get("/holidays", response_model=list[HolidayResponse])
async def list_all_holidays(
    uow: UnitOfWork = Depends(get_uow),
) -> list[HolidayResponse]:
    """List all scheduled holidays across all active terms."""
    async with uow:
        all_holidays = await uow.academic_terms.list_all_holidays()
    return [
        HolidayResponse(
            id=h.id,
            academic_term_id=h.academic_term_id,
            date=h.date,
            label=h.label,
        )
        for h in sorted(all_holidays, key=lambda x: x.date)
    ]


@router.get("/faculty/{profile_id}", response_model=FacultyProfileResponse)
async def get_faculty_profile(
    profile_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
) -> FacultyProfileResponse:
    """Retrieve details for a single faculty profile."""
    async with uow:
        p = await uow.faculty_profiles.get_by_id(profile_id)
        if p is None:
            raise NotFoundError("Faculty profile not found")
    return FacultyProfileResponse(
        id=p.id,
        user_id=p.user_id,
        department_id=p.department_id,
        full_name=p.full_name,
        initials=p.initials.value,
        aliases=list(p.aliases),
        email=p.email,
        phone=p.phone,
    )


@router.post(
    "/faculty",
    response_model=FacultyProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_faculty(
    payload: CreateFacultyRequest,
    principal: Principal = Depends(require_hod_or_admin),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> FacultyProfileResponse:
    """Create a new faculty account and profile."""
    use_case = CreateFacultyUseCase(uow, clock)
    profile = await use_case.execute(
        principal=principal,
        department_id=payload.department_id,
        full_name=payload.full_name,
        initials_str=payload.initials,
        email=payload.email,
        aliases=tuple(payload.aliases),
        phone=payload.phone,
        initial_password=payload.initial_password,
    )
    return FacultyProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        department_id=profile.department_id,
        full_name=profile.full_name,
        initials=profile.initials.value,
        aliases=list(profile.aliases),
        email=profile.email,
        phone=profile.phone,
    )


@router.put("/faculty/{profile_id}", response_model=FacultyProfileResponse)
async def update_faculty(
    profile_id: UUID,
    payload: UpdateFacultyRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> FacultyProfileResponse:
    """Update details of an existing faculty member."""
    use_case = UpdateFacultyUseCase(uow, clock)
    aliases_tuple = tuple(payload.aliases) if payload.aliases is not None else None
    profile = await use_case.execute(
        principal=principal,
        profile_id=profile_id,
        full_name=payload.full_name,
        initials_str=payload.initials,
        aliases=aliases_tuple,
        phone=payload.phone,
    )
    return FacultyProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        department_id=profile.department_id,
        full_name=profile.full_name,
        initials=profile.initials.value,
        aliases=list(profile.aliases),
        email=profile.email,
        phone=profile.phone,
    )


@router.delete("/faculty/{profile_id}", response_model=StatusResponse)
async def deactivate_faculty(
    profile_id: UUID,
    principal: Principal = Depends(require_hod_or_admin),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> StatusResponse:
    """Deactivate a faculty member, preventing future logins."""
    use_case = DeactivateFacultyUseCase(uow, clock)
    await use_case.execute(principal, profile_id)
    return StatusResponse(status="deactivated")


@router.post("/faculty/bulk-import", response_model=BulkImportResponse)
async def bulk_import_faculty(
    department_id: UUID = Form(...),
    file: UploadFile = File(...),
    principal: Principal = Depends(require_hod_or_admin),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> BulkImportResponse:
    """Bulk import faculty records from a CSV or XLSX spreadsheet."""
    filename = file.filename or "upload.csv"
    ext = filename.split(".")[-1].lower() if "." in filename else "csv"
    if ext not in ("csv", "xlsx"):
        raise ValidationError("File must be CSV or XLSX")

    content = await file.read()
    use_case = BulkImportFacultyUseCase(uow, clock)
    report = await use_case.execute(
        principal=principal,
        department_id=department_id,
        file_content=content,
        file_extension=ext,
    )

    return BulkImportResponse(
        total_rows=report.total_rows,
        created_count=report.created_count,
        updated_count=report.updated_count,
        rejected_count=report.rejected_count,
        rows=[
            RowImportResultResponse(
                row_number=r.row_number,
                status=r.status,
                message=r.message,
                email=r.email,
                initials=r.initials,
            )
            for r in report.rows
        ],
    )


@router.get("/terms", response_model=list[AcademicTermResponse])
async def list_terms(
    uow: UnitOfWork = Depends(get_uow),
) -> list[AcademicTermResponse]:
    """List academic terms."""
    today = date.today()
    async with uow:
        active = await uow.academic_terms.get_active_term(today)
    if active:
        return [
            AcademicTermResponse(
                id=active.id,
                name=active.name,
                start_date=active.start_date,
                end_date=active.end_date,
                timezone=active.timezone,
            )
        ]
    return []


@router.post(
    "/terms",
    response_model=AcademicTermResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_term(
    payload: CreateAcademicTermRequest,
    principal: Principal = Depends(require_admin),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> AcademicTermResponse:
    """Create a new academic calendar term."""
    use_case = ManageTermsUseCase(uow, clock)
    term = await use_case.create_term(
        principal=principal,
        name=payload.name,
        start_date=payload.start_date,
        end_date=payload.end_date,
        timezone=payload.timezone,
    )
    return AcademicTermResponse(
        id=term.id,
        name=term.name,
        start_date=term.start_date,
        end_date=term.end_date,
        timezone=term.timezone,
    )


@router.get("/terms/{term_id}/holidays", response_model=list[HolidayResponse])
async def list_holidays(
    term_id: UUID,
    uow: UnitOfWork = Depends(get_uow),
) -> list[HolidayResponse]:
    """List all scheduled holidays for an academic term."""
    async with uow:
        holidays = await uow.academic_terms.list_holidays(term_id)
    return [
        HolidayResponse(
            id=h.id,
            academic_term_id=h.academic_term_id,
            date=h.date,
            label=h.label,
        )
        for h in holidays
    ]


@router.post(
    "/terms/{term_id}/holidays",
    response_model=HolidayResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_holiday(
    term_id: UUID,
    payload: CreateHolidayRequest,
    principal: Principal = Depends(require_admin),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> HolidayResponse:
    """Add a holiday date to an academic term."""
    use_case = ManageTermsUseCase(uow, clock)
    holiday = await use_case.add_holiday(
        principal=principal,
        term_id=term_id,
        holiday_date=payload.date,
        label=payload.label,
    )
    return HolidayResponse(
        id=holiday.id,
        academic_term_id=holiday.academic_term_id,
        date=holiday.date,
        label=holiday.label,
    )


@router.post(
    "/terms/{term_id}/holidays/bulk",
    response_model=list[HolidayResponse],
    status_code=status.HTTP_201_CREATED,
)
async def bulk_import_holidays(
    term_id: UUID,
    file: UploadFile = File(...),
    principal: Principal = Depends(require_admin),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> list[HolidayResponse]:
    """Bulk import holidays from a CSV file."""
    content = await file.read()
    use_case = ManageTermsUseCase(uow, clock)
    holidays = await use_case.bulk_import_holidays(
        principal=principal,
        term_id=term_id,
        csv_content=content,
    )
    return [
        HolidayResponse(
            id=h.id,
            academic_term_id=h.academic_term_id,
            date=h.date,
            label=h.label,
        )
        for h in holidays
    ]
