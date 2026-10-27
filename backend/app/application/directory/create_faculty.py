from uuid import UUID, uuid4

from app.application.security.policy import AuthorisationPolicy, Principal
from app.core.clock import Clock
from app.core.errors import ConflictError
from app.core.security import hash_password
from app.domain import (
    AuditLog,
    FacultyProfile,
    Initials,
    Role,
    UnitOfWork,
    User,
)


class CreateFacultyUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock

    async def execute(
        self,
        principal: Principal,
        department_id: UUID,
        full_name: str,
        initials_str: str,
        email: str,
        aliases: tuple[str, ...] = (),
        phone: str | None = None,
        initial_password: str = "FacultyDesk123!",
    ) -> FacultyProfile:
        AuthorisationPolicy.enforce(
            principal, resource_dept_id=department_id, action="create_faculty"
        )
        initials = Initials(initials_str)
        cleaned_email = email.strip().lower()

        async with self._uow:
            dept = await self._uow.departments.get_by_id(department_id)
            if dept is None:
                raise ConflictError(f"Department {department_id} does not exist")

            existing_user = await self._uow.users.get_by_email(cleaned_email)
            if existing_user is not None:
                raise ConflictError(f"User with email '{cleaned_email}' already exists")

            existing_init = await self._uow.faculty_profiles.get_by_department_and_initials(
                department_id, initials
            )
            if existing_init is not None:
                msg = (
                    f"Initials '{initials.value}' are already registered "
                    f"in department {dept.code}"
                )
                raise ConflictError(msg)

            user = User(
                id=uuid4(),
                email=cleaned_email,
                password_hash=hash_password(initial_password),
                role=Role.FACULTY,
                is_active=True,
            )
            await self._uow.users.save(user)

            profile = FacultyProfile(
                id=uuid4(),
                user_id=user.id,
                department_id=department_id,
                full_name=full_name.strip(),
                initials=initials,
                aliases=aliases,
                email=cleaned_email,
                phone=phone.strip() if phone else None,
            )
            saved_profile = await self._uow.faculty_profiles.save(profile)

            audit = AuditLog(
                id=uuid4(),
                user_id=principal.user_id,
                action="CREATE_FACULTY",
                resource_type="FacultyProfile",
                resource_id=str(saved_profile.id),
                payload={
                    "department_id": str(department_id),
                    "email": cleaned_email,
                    "initials": initials.value,
                },
                timestamp_utc=self._clock.now(),
            )
            await self._uow.audit_logs.save(audit)
            await self._uow.commit()

            return saved_profile
