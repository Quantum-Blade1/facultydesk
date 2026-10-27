from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.application.security.policy import Principal
from app.core.clock import Clock, SystemClock
from app.core.db import async_session_factory
from app.core.errors import ForbiddenError, UnauthorizedError
from app.core.redis import get_redis_client
from app.core.security import decode_token
from app.domain import Role, UnitOfWork
from app.infrastructure.db.repositories import SqlAlchemyUnitOfWork
from app.infrastructure.security.rate_limiter import RedisSlidingWindowRateLimiter

_bearer_scheme = HTTPBearer(auto_error=False)


def get_uow() -> UnitOfWork:
    return SqlAlchemyUnitOfWork(async_session_factory)


def get_clock() -> Clock:
    return SystemClock()


def get_rate_limiter() -> RedisSlidingWindowRateLimiter:
    return RedisSlidingWindowRateLimiter(get_redis_client())


async def get_current_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> Principal:
    if credentials is None:
        raise UnauthorizedError("Missing or invalid Authorization header")

    try:
        payload = decode_token(credentials.credentials)
    except jwt.PyJWTError as exc:
        raise UnauthorizedError(f"Invalid access token: {exc}") from exc

    if payload.get("type") != "access":
        raise UnauthorizedError("Invalid token type")

    try:
        user_id = UUID(payload["sub"])
        role = Role(payload["role"])
        dept_str = payload.get("dept")
        dept_id = UUID(dept_str) if dept_str else None
    except (KeyError, ValueError) as exc:
        raise UnauthorizedError("Malformed token claims") from exc

    return Principal(user_id=user_id, role=role, department_id=dept_id)


def require_admin(principal: Principal = Depends(get_current_principal)) -> Principal:
    if principal.role != Role.ADMIN:
        raise ForbiddenError("Administrator access required")
    return principal


def require_hod_or_admin(
    principal: Principal = Depends(get_current_principal),
) -> Principal:
    if principal.role not in (Role.ADMIN, Role.HOD):
        raise ForbiddenError("HOD or Administrator access required")
    return principal
