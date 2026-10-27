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
)
from app.domain import RefreshToken, UnitOfWork


@dataclass(frozen=True)
class RefreshResult:
    access_token: str
    refresh_token: str


class RefreshTokenUseCase:
    def __init__(self, uow: UnitOfWork, clock: Clock) -> None:
        self._uow = uow
        self._clock = clock
        self._settings = get_settings()

    async def execute(self, raw_refresh_token: str) -> RefreshResult:
        token_hash = hash_refresh_token(raw_refresh_token)
        now = self._clock.now()

        async with self._uow:
            token = await self._uow.refresh_tokens.get_by_hash(token_hash)
            if token is None:
                raise UnauthorizedError("Invalid refresh token")

            if token.is_revoked:
                await self._uow.refresh_tokens.revoke_family(token.family_id)
                await self._uow.commit()
                raise UnauthorizedError(
                    "Compromised refresh token presented: entire token family revoked"
                )

            if now >= token.expires_at_utc:
                raise UnauthorizedError("Refresh token expired")

            user = await self._uow.users.get_by_id(token.user_id)
            if user is None or not user.is_active:
                raise UnauthorizedError("User is inactive or deleted")

            token.revoke()
            await self._uow.refresh_tokens.save(token)

            new_raw_token = generate_refresh_token()
            new_hash = hash_refresh_token(new_raw_token)
            expires_at = now + timedelta(days=self._settings.REFRESH_TOKEN_EXPIRE_DAYS)

            child_token = RefreshToken(
                id=uuid4(),
                user_id=token.user_id,
                token_hash=new_hash,
                family_id=token.family_id,
                is_revoked=False,
                expires_at_utc=expires_at,
                created_at_utc=now,
            )
            await self._uow.refresh_tokens.save(child_token)

            profile = await self._uow.faculty_profiles.get_by_user_id(user.id)
            dept_id_str = str(profile.department_id) if profile else None

            new_access_token = create_access_token(
                subject=str(user.id),
                role=user.role.value,
                department_id=dept_id_str,
                clock=self._clock,
            )

            await self._uow.commit()

            return RefreshResult(
                access_token=new_access_token,
                refresh_token=new_raw_token,
            )
