from app.core.security import hash_refresh_token
from app.domain import UnitOfWork


class LogoutUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, raw_refresh_token: str | None) -> None:
        if not raw_refresh_token:
            return

        token_hash = hash_refresh_token(raw_refresh_token)
        async with self._uow:
            token = await self._uow.refresh_tokens.get_by_hash(token_hash)
            if token is not None:
                await self._uow.refresh_tokens.revoke_family(token.family_id)
                await self._uow.commit()
