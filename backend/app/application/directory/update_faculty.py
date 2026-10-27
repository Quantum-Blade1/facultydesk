from uuid import UUID

from app.application.security.policy import AuthorisationPolicy, Principal
from app.core.clock import Clock
from app.core.errors import ConflictError, NotFoundError
from app.domain import (
    AuditLog,
    FacultyProfile,
    Initials,
    UnitOfWork,
)


class UpdateFacultyUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        principal: Principal,
        profile_id: UUID,
        full_name: str | None = None,
        initials_str: str | None = None,
        aliases: tuple[str, ...] | None = None,
        phone: str | None = None,
    ) -> FacultyProfile:
        async with self._uow:
            profile = await self._uow.faculty_profiles.get_by_id(profile_id)
            if profile is None:
                raise NotFoundError("Faculty profile not found")

            AuthorisationPolicy.enforce(
                principal,
                resource_owner_id=profile.user_id,
                resource_dept_id=profile.department_id,
                action="update_faculty",
            )

            if initials_str is not None:
                new_initials = Initials(initials_str)
                if new_initials.value != profile.initials.value:
                    existing = await self._uow.faculty_profiles.get_by_department_and_initials(
                        profile.department_id, new_initials
                    )
                    if existing is not None and existing.id != profile.id:
                        msg = (
                            f"Initials '{new_initials.value}' are already taken in this department"
                        )
                        raise ConflictError(msg)
                    profile.initials = new_initials

            if full_name is not None:
                profile.full_name = full_name.strip()
            if aliases is not None:
                profile.aliases = aliases
            if phone is not None:
                profile.phone = phone.strip() if phone else None

            saved = await self._uow.faculty_profiles.save(profile)

            audit = AuditLog(
                user_id=principal.user_id,
                action="UPDATE_FACULTY",
                resource_type="FacultyProfile",
                resource_id=str(saved.id),
                payload={"initials": saved.initials.value, "full_name": saved.full_name},
                timestamp_utc=self._clock.now(),
            )
            await self._uow.audit_logs.save(audit)
            await self._uow.commit()

            return saved
