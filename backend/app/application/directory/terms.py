import csv
import io
from datetime import date, datetime
from uuid import UUID, uuid4

from app.application.security.policy import AuthorisationPolicy, Principal
from app.core.clock import Clock
from app.core.errors import NotFoundError
from app.domain import AcademicTerm, AuditLog, Holiday, UnitOfWork


class ManageTermsUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def create_term(
        self,
        principal: Principal,
        name: str,
        start_date: date,
        end_date: date,
        timezone: str = "Asia/Kolkata",
    ) -> AcademicTerm:
        AuthorisationPolicy.enforce(principal, action="manage_terms")
        async with self._uow:
            term = AcademicTerm(
                id=uuid4(),
                name=name.strip(),
                start_date=start_date,
                end_date=end_date,
                timezone=timezone,
            )
            saved = await self._uow.academic_terms.save(term)

            audit = AuditLog(
                user_id=principal.user_id,
                action="CREATE_ACADEMIC_TERM",
                resource_type="AcademicTerm",
                resource_id=str(saved.id),
                payload={
                    "name": saved.name,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                },
                timestamp_utc=self._clock.now(),
            )
            await self._uow.audit_logs.save(audit)
            await self._uow.commit()

            return saved

    async def add_holiday(
        self,
        principal: Principal,
        term_id: UUID,
        holiday_date: date,
        label: str,
    ) -> Holiday:
        AuthorisationPolicy.enforce(principal, action="manage_terms")
        async with self._uow:
            term = await self._uow.academic_terms.get_by_id(term_id)
            if term is None:
                raise NotFoundError("Academic term not found")

            holiday = Holiday(
                id=uuid4(),
                academic_term_id=term_id,
                date=holiday_date,
                label=label.strip(),
            )
            saved = await self._uow.academic_terms.save_holiday(holiday)

            audit = AuditLog(
                user_id=principal.user_id,
                action="ADD_HOLIDAY",
                resource_type="Holiday",
                resource_id=str(saved.id),
                payload={"date": str(holiday_date), "label": saved.label},
                timestamp_utc=self._clock.now(),
            )
            await self._uow.audit_logs.save(audit)
            await self._uow.commit()

            return saved

    async def bulk_import_holidays(
        self,
        principal: Principal,
        term_id: UUID,
        csv_content: bytes,
    ) -> list[Holiday]:
        AuthorisationPolicy.enforce(principal, action="manage_terms")
        text = csv_content.decode("utf-8-sig", errors="replace")
        reader = csv.DictReader(io.StringIO(text))

        imported_holidays: list[Holiday] = []
        async with self._uow:
            term = await self._uow.academic_terms.get_by_id(term_id)
            if term is None:
                raise NotFoundError("Academic term not found")

            for r in reader:
                d_str = r.get("date", "").strip()
                lbl = r.get("label", "").strip()
                if not d_str or not lbl:
                    continue
                parsed_d = datetime.strptime(d_str, "%Y-%m-%d").date()
                holiday = Holiday(
                    id=uuid4(),
                    academic_term_id=term_id,
                    date=parsed_d,
                    label=lbl,
                )
                saved = await self._uow.academic_terms.save_holiday(holiday)
                imported_holidays.append(saved)

            audit = AuditLog(
                user_id=principal.user_id,
                action="BULK_IMPORT_HOLIDAYS",
                resource_type="AcademicTerm",
                resource_id=str(term_id),
                payload={"count": len(imported_holidays)},
                timestamp_utc=self._clock.now(),
            )
            await self._uow.audit_logs.save(audit)
            await self._uow.commit()

        return imported_holidays
