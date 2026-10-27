from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, Request, Response
from pydantic import BaseModel

from app.api.deps import (
    get_clock,
    get_current_principal,
    get_rate_limiter,
    get_uow,
)
from app.application.auth.change_password import ChangePasswordUseCase
from app.application.auth.login import LoginUseCase
from app.application.auth.logout import LogoutUseCase
from app.application.auth.refresh import RefreshTokenUseCase
from app.application.security.policy import Principal
from app.core.clock import Clock
from app.core.config import get_settings
from app.core.errors import NotFoundError, UnauthorizedError
from app.domain import UnitOfWork
from app.infrastructure.security.rate_limiter import RedisSlidingWindowRateLimiter

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


class LoginRequest(BaseModel):
    email: str
    password: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    role: str
    is_active: bool


class ProfileResponse(BaseModel):
    id: UUID
    department_id: UUID
    full_name: str
    initials: str
    aliases: list[str]
    email: str
    phone: str | None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    profile: ProfileResponse | None


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class StatusResponse(BaseModel):
    status: str


class CurrentUserResponse(BaseModel):
    user: UserResponse
    profile: ProfileResponse | None


def _get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"


@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
    limiter: RedisSlidingWindowRateLimiter = Depends(get_rate_limiter),
) -> LoginResponse:
    """Authenticate with email and password, establishing an access token and refresh cookie."""
    client_ip = _get_client_ip(request)
    normalized_email = payload.email.strip().lower()

    await limiter.check_and_consume(f"ratelimit:login:ip:{client_ip}", limit=5, window_seconds=60)
    await limiter.check_and_consume(
        f"ratelimit:login:account:{normalized_email}", limit=5, window_seconds=60
    )

    use_case = LoginUseCase(uow, clock)
    result = await use_case.execute(normalized_email, payload.password)

    is_production = settings.ENVIRONMENT == "production"
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=is_production,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/api/auth",
    )

    profile_dto = (
        ProfileResponse(
            id=result.profile.id,
            department_id=result.profile.department_id,
            full_name=result.profile.full_name,
            initials=result.profile.initials.value,
            aliases=list(result.profile.aliases),
            email=result.profile.email,
            phone=result.profile.phone,
        )
        if result.profile
        else None
    )

    return LoginResponse(
        access_token=result.access_token,
        user=UserResponse(
            id=result.user.id,
            email=result.user.email,
            role=result.user.role.value,
            is_active=result.user.is_active,
        ),
        profile=profile_dto,
    )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_tokens(
    request: Request,
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
    limiter: RedisSlidingWindowRateLimiter = Depends(get_rate_limiter),
) -> RefreshResponse:
    """Rotate refresh token and issue a fresh access token."""
    client_ip = _get_client_ip(request)
    await limiter.check_and_consume(
        f"ratelimit:refresh:ip:{client_ip}", limit=30, window_seconds=60
    )

    raw_token = refresh_token or request.headers.get("X-Refresh-Token")
    if not raw_token:
        raise UnauthorizedError("Missing refresh token cookie")

    use_case = RefreshTokenUseCase(uow, clock)
    result = await use_case.execute(raw_token)

    is_production = settings.ENVIRONMENT == "production"
    response.set_cookie(
        key="refresh_token",
        value=result.refresh_token,
        httponly=True,
        secure=is_production,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/api/auth",
    )

    return RefreshResponse(access_token=result.access_token)


@router.post("/logout", response_model=StatusResponse)
async def logout(
    request: Request,
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    uow: UnitOfWork = Depends(get_uow),
) -> StatusResponse:
    """Revoke refresh token family and delete refresh cookie."""
    raw_token = refresh_token or request.headers.get("X-Refresh-Token")
    use_case = LogoutUseCase(uow)
    await use_case.execute(raw_token)

    response.delete_cookie(key="refresh_token", path="/api/auth")
    return StatusResponse(status="logged_out")


@router.post("/change-password", response_model=StatusResponse)
async def change_password(
    payload: ChangePasswordRequest,
    response: Response,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> StatusResponse:
    """Update current user password and invalidate active sessions."""
    use_case = ChangePasswordUseCase(uow)
    await use_case.execute(principal.user_id, payload.current_password, payload.new_password)
    response.delete_cookie(key="refresh_token", path="/api/auth")
    return StatusResponse(status="password_changed")


@router.get("/me", response_model=CurrentUserResponse)
async def get_me(
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> CurrentUserResponse:
    """Retrieve profile and identity details of the authenticated caller."""
    async with uow:
        user = await uow.users.get_by_id(principal.user_id)
        if user is None:
            raise NotFoundError("User not found")
        profile = await uow.faculty_profiles.get_by_user_id(principal.user_id)

    profile_dto = (
        ProfileResponse(
            id=profile.id,
            department_id=profile.department_id,
            full_name=profile.full_name,
            initials=profile.initials.value,
            aliases=list(profile.aliases),
            email=profile.email,
            phone=profile.phone,
        )
        if profile
        else None
    )

    return CurrentUserResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            role=user.role.value,
            is_active=user.is_active,
        ),
        profile=profile_dto,
    )
