from datetime import time
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, Field

from app.api.deps import get_current_principal, get_uow
from app.application.reminders.use_cases import (
    DeletePushSubscriptionUseCase,
    GetUpcomingNotificationsUseCase,
    GetUserQuietHoursUseCase,
    GetUserReminderRulesUseCase,
    RegisterPushSubscriptionUseCase,
    UpdateReminderRuleUseCase,
    UpdateUserQuietHoursUseCase,
)
from app.application.security.policy import Principal
from app.core.config import get_settings
from app.core.errors import NotFoundError
from app.domain.entities import PushSubscription, ReminderRule, ScheduledNotification
from app.domain.repositories import UnitOfWork
from app.domain.value_objects import EventKind, NotificationChannel, QuietHours

router = APIRouter(prefix="/reminders", tags=["reminders"])


class ReminderRuleResponse(BaseModel):
    id: UUID
    user_id: UUID
    event_kind: str
    offsets_minutes: list[int]
    channels: list[str]

    @classmethod
    def from_domain(cls, rule: ReminderRule) -> "ReminderRuleResponse":
        return cls(
            id=rule.id,
            user_id=rule.user_id,
            event_kind=rule.event_kind.value,
            offsets_minutes=list(rule.offsets_minutes),
            channels=[c.value for c in rule.channels],
        )


class UpdateReminderRuleRequest(BaseModel):
    event_kind: EventKind
    offsets_minutes: list[int] = Field(..., min_length=1)
    channels: list[NotificationChannel] = Field(..., min_length=1)


class QuietHoursResponse(BaseModel):
    start_time: str | None
    end_time: str | None

    @classmethod
    def from_domain(cls, qh: QuietHours | None) -> "QuietHoursResponse":
        if qh is None:
            return cls(start_time=None, end_time=None)
        return cls(
            start_time=qh.start_time.isoformat() if qh.start_time else None,
            end_time=qh.end_time.isoformat() if qh.end_time else None,
        )


class UpdateQuietHoursRequest(BaseModel):
    start_time: time | None = None
    end_time: time | None = None


class PushSubscriptionRequest(BaseModel):
    endpoint: str = Field(..., min_length=1)
    p256dh: str = Field(..., min_length=1)
    auth: str = Field(..., min_length=1)


class DeletePushSubscriptionRequest(BaseModel):
    endpoint: str = Field(..., min_length=1)


class PushSubscriptionResponse(BaseModel):
    id: UUID
    user_id: UUID
    endpoint: str

    @classmethod
    def from_domain(cls, sub: PushSubscription) -> "PushSubscriptionResponse":
        return cls(
            id=sub.id,
            user_id=sub.user_id,
            endpoint=sub.endpoint,
        )


class ScheduledNotificationResponse(BaseModel):
    id: UUID
    target_id: UUID
    target_kind: str
    channel: str
    fire_at_utc: str
    status: str
    attempts: int
    delivered_at_utc: str | None

    @classmethod
    def from_domain(cls, n: ScheduledNotification) -> "ScheduledNotificationResponse":
        return cls(
            id=n.id,
            target_id=n.target_id,
            target_kind=n.target_kind,
            channel=n.channel.value,
            fire_at_utc=n.fire_at_utc.isoformat(),
            status=n.status.value,
            attempts=n.attempts,
            delivered_at_utc=n.delivered_at_utc.isoformat() if n.delivered_at_utc else None,
        )


@router.get("/rules", response_model=list[ReminderRuleResponse])
async def get_reminder_rules(
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> list[ReminderRuleResponse]:
    """Retrieve all configurable reminder rules for the authenticated user."""
    rules = await GetUserReminderRulesUseCase(uow).execute(principal.user_id)
    return [ReminderRuleResponse.from_domain(r) for r in rules]


@router.post("/rules", response_model=ReminderRuleResponse)
async def update_reminder_rule(
    body: UpdateReminderRuleRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> ReminderRuleResponse:
    """Create or update a reminder rule for a specific event kind."""
    rule = await UpdateReminderRuleUseCase(uow).execute(
        user_id=principal.user_id,
        event_kind=body.event_kind,
        offsets_minutes=body.offsets_minutes,
        channels=body.channels,
    )
    return ReminderRuleResponse.from_domain(rule)


@router.get("/quiet-hours", response_model=QuietHoursResponse)
async def get_quiet_hours(
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> QuietHoursResponse:
    """Retrieve quiet hours window for the authenticated user."""
    try:
        qh = await GetUserQuietHoursUseCase(uow).execute(principal.user_id)
        return QuietHoursResponse.from_domain(qh)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err)) from err


@router.post("/quiet-hours", response_model=QuietHoursResponse)
async def update_quiet_hours(
    body: UpdateQuietHoursRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> QuietHoursResponse:
    """Update or clear quiet hours window for the authenticated user."""
    if (body.start_time is None) != (body.end_time is None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Both start_time and end_time must be provided, or both omitted.",
        )
    try:
        qh = await UpdateUserQuietHoursUseCase(uow).execute(
            user_id=principal.user_id,
            start_time=body.start_time,
            end_time=body.end_time,
        )
        return QuietHoursResponse.from_domain(qh)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err)) from err


@router.post("/push-subscription", response_model=PushSubscriptionResponse)
async def register_push_subscription(
    body: PushSubscriptionRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> PushSubscriptionResponse:
    """Register or refresh a WebPush subscription endpoint for the current user."""
    sub = await RegisterPushSubscriptionUseCase(uow).execute(
        user_id=principal.user_id,
        endpoint=body.endpoint,
        p256dh=body.p256dh,
        auth=body.auth,
    )
    return PushSubscriptionResponse.from_domain(sub)


@router.delete("/push-subscription", status_code=status.HTTP_204_NO_CONTENT)
async def delete_push_subscription(
    body: DeletePushSubscriptionRequest,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> Response:
    """Unregister a WebPush subscription endpoint."""
    await DeletePushSubscriptionUseCase(uow).execute(body.endpoint)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/upcoming", response_model=list[ScheduledNotificationResponse])
async def get_upcoming_notifications(
    limit: int = Query(50, ge=1, le=200),
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
) -> list[ScheduledNotificationResponse]:
    """List pending scheduled notifications for the authenticated user."""
    notifications = await GetUpcomingNotificationsUseCase(uow).execute(
        principal.user_id, limit=limit
    )
    return [ScheduledNotificationResponse.from_domain(n) for n in notifications]


class VapidPublicKeyResponse(BaseModel):
    public_key: str


@router.get("/vapid-public-key", response_model=VapidPublicKeyResponse)
async def get_vapid_public_key() -> VapidPublicKeyResponse:
    """Retrieve the application VAPID public key for WebPush subscriptions."""
    settings = get_settings()
    return VapidPublicKeyResponse(public_key=settings.VAPID_PUBLIC_KEY)
