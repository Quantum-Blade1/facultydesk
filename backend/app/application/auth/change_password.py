from uuid import UUID

from app.core.errors import NotFoundError, UnauthorizedError
from app.core.security import hash_password, verify_password
from app.domain import UnitOfWork


class ChangePasswordUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, user_id: UUID, old_password: str, new_password: str) -> None:
        if len(new_password) < 8:
            raise UnauthorizedError("New password must be at least 8 characters")

        async with self._uow:
            user = await self._uow.users.get_by_id(user_id)
            if user is None:
                raise NotFoundError("User not found")

            if not verify_password(user.password_hash, old_password):
                raise UnauthorizedError("Current password incorrect")

            user.password_hash = hash_password(new_password)
            await self._uow.users.save(user)
            await self._uow.refresh_tokens.revoke_all_for_user(user_id)
            await self._uow.commit()
