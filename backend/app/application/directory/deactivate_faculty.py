from uuid import UUID

from app.application.security.policy import AuthorisationPolicy, Principal
from app.core.clock import Clock
from app.core.errors import NotFoundError
from app.domain import AuditLog, UnitOfWork


class DeactivateFacultyUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(self, principal: Principal, profile_id: UUID) -> None:
        async with self._uow:
            profile = await self._uow.faculty_profiles.get_by_id(profile_id)
            if profile is None:
                raise NotFoundError("Faculty profile not found")

            AuthorisationPolicy.enforce(
                principal,
                resource_dept_id=profile.department_id,
                action="deactivate_faculty",
            )

            user = await self._uow.users.get_by_id(profile.user_id)
            if user is not None:
                user.is_active = False
                await self._uow.users.save(user)
                await self._uow.refresh_tokens.revoke_all_for_user(user.id)

            audit = AuditLog(
                user_id=principal.user_id,
                action="DEACTIVATE_FACULTY",
                resource_type="FacultyProfile",
                resource_id=str(profile.id),
                payload={"user_id": str(profile.user_id)},
                timestamp_utc=self._clock.now(),
            )
            await self._uow.audit_logs.save(audit)
            await self._uow.commit()
