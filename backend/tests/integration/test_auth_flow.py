from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.application.auth.change_password import ChangePasswordUseCase
from app.application.auth.login import LoginUseCase
from app.application.auth.logout import LogoutUseCase
from app.application.auth.refresh import RefreshTokenUseCase
from app.core.clock import FrozenClock
from app.core.db import async_session_factory
from app.core.errors import UnauthorizedError
from app.core.security import decode_token, hash_password
from app.domain import Role, User
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork


@pytest.mark.asyncio
async def test_auth_login_and_token_rotation() -> None:
    uow = SqlAlchemyUnitOfWork(async_session_factory)
    clock = FrozenClock(datetime.now(UTC))
    email = f"auth_test_{uuid4().hex[:6]}@college.edu"
    raw_password = "SecurePassword123!"

    async with uow:
        user = User(
            id=uuid4(),
            email=email,
            password_hash=hash_password(raw_password),
            role=Role.FACULTY,
            is_active=True,
        )
        await uow.users.save(user)
        await uow.commit()

    login_use_case = LoginUseCase(uow, clock)
    login_result = await login_use_case.execute(email, raw_password)

    assert login_result.access_token is not None
    assert login_result.refresh_token is not None

    claims = decode_token(login_result.access_token)
    assert claims["sub"] == str(user.id)
    assert claims["role"] == Role.FACULTY.value
    assert claims["type"] == "access"

    refresh_use_case = RefreshTokenUseCase(uow, clock)
    first_refresh = await refresh_use_case.execute(login_result.refresh_token)

    assert first_refresh.access_token is not None
    assert first_refresh.refresh_token != login_result.refresh_token

    second_refresh = await refresh_use_case.execute(first_refresh.refresh_token)
    assert second_refresh.access_token is not None
    assert second_refresh.refresh_token != first_refresh.refresh_token


@pytest.mark.asyncio
async def test_refresh_token_reuse_revokes_entire_family() -> None:
    uow = SqlAlchemyUnitOfWork(async_session_factory)
    clock = FrozenClock(datetime.now(UTC))
    email = f"reuse_test_{uuid4().hex[:6]}@college.edu"
    raw_password = "SecurePassword123!"

    async with uow:
        user = User(
            id=uuid4(),
            email=email,
            password_hash=hash_password(raw_password),
            role=Role.FACULTY,
            is_active=True,
        )
        await uow.users.save(user)
        await uow.commit()

    login_use_case = LoginUseCase(uow, clock)
    login_result = await login_use_case.execute(email, raw_password)
    token_t0 = login_result.refresh_token

    refresh_use_case = RefreshTokenUseCase(uow, clock)
    result_t1 = await refresh_use_case.execute(token_t0)
    token_t1 = result_t1.refresh_token

    with pytest.raises(UnauthorizedError) as exc_info:
        await refresh_use_case.execute(token_t0)
    assert "Compromised" in str(exc_info.value.message)

    with pytest.raises(UnauthorizedError):
        await refresh_use_case.execute(token_t1)


@pytest.mark.asyncio
async def test_logout_and_password_change_revoke_sessions() -> None:
    uow = SqlAlchemyUnitOfWork(async_session_factory)
    clock = FrozenClock(datetime.now(UTC))
    email = f"session_test_{uuid4().hex[:6]}@college.edu"
    raw_password = "InitialPassword123!"
    new_password = "UpdatedPassword123!"

    async with uow:
        user = User(
            id=uuid4(),
            email=email,
            password_hash=hash_password(raw_password),
            role=Role.FACULTY,
            is_active=True,
        )
        await uow.users.save(user)
        await uow.commit()

    login_use_case = LoginUseCase(uow, clock)
    login_result = await login_use_case.execute(email, raw_password)

    logout_use_case = LogoutUseCase(uow)
    await logout_use_case.execute(login_result.refresh_token)

    refresh_use_case = RefreshTokenUseCase(uow, clock)
    with pytest.raises(UnauthorizedError):
        await refresh_use_case.execute(login_result.refresh_token)

    login_result_2 = await login_use_case.execute(email, raw_password)
    change_pass_use_case = ChangePasswordUseCase(uow)
    await change_pass_use_case.execute(user.id, raw_password, new_password)

    with pytest.raises(UnauthorizedError):
        await refresh_use_case.execute(login_result_2.refresh_token)

    login_result_3 = await login_use_case.execute(email, new_password)
    assert login_result_3.access_token is not None
