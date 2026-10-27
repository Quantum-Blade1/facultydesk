from dataclasses import dataclass
from datetime import timedelta
from uuid import uuid4

from app.core.clock import Clock
from app.core.config import get_settings
from app.core.errors import UnauthorizedError
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
    verify_password,
)
from app.domain import FacultyProfile, RefreshToken, UnitOfWork, User


@dataclass(frozen=True)
class LoginResult:
    access_token: str
    refresh_token: str
    user: User
    profile: FacultyProfile | None


class LoginUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock
        self._settings = get_settings()

    async def execute(self, email: str, password: str) -> LoginResult:
        async with self._uow:
            user = await self._uow.users.get_by_email(email.strip().lower())
            if user is None or not user.is_active:
                raise UnauthorizedError("Invalid email or password")

            if not verify_password(user.password_hash, password):
                raise UnauthorizedError("Invalid email or password")

            profile = await self._uow.faculty_profiles.get_by_user_id(user.id)
            dept_id_str = str(profile.department_id) if profile else None

            access_token = create_access_token(
                subject=str(user.id),
                role=user.role.value,
                department_id=dept_id_str,
                clock=self._clock,
            )

            raw_refresh = generate_refresh_token()
            token_hash = hash_refresh_token(raw_refresh)
            now = self._clock.now()
            expires_at = now + timedelta(days=self._settings.REFRESH_TOKEN_EXPIRE_DAYS)

            refresh_entity = RefreshToken(
                id=uuid4(),
                user_id=user.id,
                token_hash=token_hash,
                family_id=uuid4(),
                is_revoked=False,
                expires_at_utc=expires_at,
                created_at_utc=now,
            )
            await self._uow.refresh_tokens.save(refresh_entity)
            await self._uow.commit()

            return LoginResult(
                access_token=access_token,
                refresh_token=raw_refresh,
                user=user,
                profile=profile,
            )
