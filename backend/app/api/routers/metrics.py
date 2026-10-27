from __future__ import annotations

from datetime import datetime
from uuid import UUID

import redis.asyncio as aioredis
import structlog
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_clock, get_current_principal, get_redis, get_uow
from app.application.security.policy import AuthorisationPolicy, Principal
from app.core.clock import Clock
from app.core.errors import NotFoundError, ValidationError
from app.core.redis import RedisClient
from app.domain import NotificationStatus, UnitOfWork

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/admin", tags=["Admin & Hardening"])


class DeadLetterResponse(BaseModel):
    id: UUID
    target_id: UUID
    target_kind: str
    user_id: UUID
    channel: str
    fire_at_utc: datetime
    attempts: int
    last_error: str | None


class LatenessPercentilesResponse(BaseModel):
    p50: float
    p95: float
    p99: float
    sample_size: int


class QueueDepthResponse(BaseModel):
    celery_default: int
    due_pending_notifications: int


class AdminMetricsResponse(BaseModel):
    notifications_by_status: dict[str, int]
    queue_depth: QueueDepthResponse
    lateness_percentiles_seconds: LatenessPercentilesResponse
    failed_dead_letters: list[DeadLetterResponse]


def compute_lateness_percentiles(
    samples: list[float], percentiles: list[float] | None = None
) -> dict[str, float]:
    targets = percentiles if percentiles is not None else [50.0, 95.0, 99.0]
    if not samples:
        return {"p50": 0.0, "p95": 0.0, "p99": 0.0}

    sorted_s = sorted(max(0.0, float(x)) for x in samples)
    n = len(sorted_s)
    res: dict[str, float] = {}

    for p in targets:
        key = f"p{int(p)}"
        if n == 1:
            res[key] = round(sorted_s[0], 2)
            continue
        k = 1.0 + (p / 100.0) * (n - 1)
        j = int(k)
        f = k - j
        if j >= n:
            res[key] = round(sorted_s[-1], 2)
        elif j < 1:
            res[key] = round(sorted_s[0], 2)
        else:
            val = sorted_s[j - 1] + f * (sorted_s[j] - sorted_s[j - 1])
            res[key] = round(val, 2)

    return res


@router.get("/metrics", response_model=AdminMetricsResponse)
async def get_system_metrics(
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    redis: RedisClient = Depends(get_redis),
    clock: Clock = Depends(get_clock),
) -> AdminMetricsResponse:
    """Retrieve system reliability metrics, queue depth, lateness percentiles, and dead-letters."""
    AuthorisationPolicy.enforce(principal, action="view_admin_metrics")

    now_utc = clock.now()
    async with uow:
        counts = await uow.notifications.count_by_status()
        lateness_samples = await uow.notifications.list_delivered_lateness_samples(5000)
        dead_letters = await uow.notifications.list_dead_letters(50)
        due_pending = len(await uow.notifications.list_due(now_utc))

    celery_len = 0
    try:
        celery_len = int(await redis.llen("celery"))
    except Exception as e:
        logger.warning("redis_llen_failed", error=str(e))

    pcts = compute_lateness_percentiles(lateness_samples)

    return AdminMetricsResponse(
        notifications_by_status=counts,
        queue_depth=QueueDepthResponse(
            celery_default=celery_len,
            due_pending_notifications=due_pending,
        ),
        lateness_percentiles_seconds=LatenessPercentilesResponse(
            p50=pcts.get("p50", 0.0),
            p95=pcts.get("p95", 0.0),
            p99=pcts.get("p99", 0.0),
            sample_size=len(lateness_samples),
        ),
        failed_dead_letters=[
            DeadLetterResponse(
                id=dl.id,
                target_id=dl.target_id,
                target_kind=dl.target_kind,
                user_id=dl.user_id,
                channel=dl.channel.value,
                fire_at_utc=dl.fire_at_utc,
                attempts=dl.attempts,
                last_error=dl.last_error,
            )
            for dl in dead_letters
        ],
    )


@router.post("/notifications/{notification_id}/retry", response_model=DeadLetterResponse)
async def retry_failed_notification(
    notification_id: UUID,
    principal: Principal = Depends(get_current_principal),
    uow: UnitOfWork = Depends(get_uow),
    clock: Clock = Depends(get_clock),
) -> DeadLetterResponse:
    """Retry a failed dead-letter notification by resetting status to PENDING."""
    AuthorisationPolicy.enforce(principal, action="retry_dead_letter")

    now_utc = clock.now()
    async with uow:
        notif = await uow.notifications.get_by_id(notification_id)
        if notif is None:
            raise NotFoundError(f"Notification {notification_id} not found")

        if notif.status != NotificationStatus.FAILED:
            msg = (
                f"Notification is in status '{notif.status.value}', "
                "only FAILED notifications can be retried"
            )
            raise ValidationError(msg)

        notif.status = NotificationStatus.PENDING
        notif.attempts = 0
        notif.fire_at_utc = now_utc
        notif.last_error = None
        saved = await uow.notifications.save(notif)
        await uow.commit()

        logger.info(
            "admin_retry_notification",
            notification_id=str(saved.id),
            admin_user_id=str(principal.user_id),
        )

        return DeadLetterResponse(
            id=saved.id,
            target_id=saved.target_id,
            target_kind=saved.target_kind,
            user_id=saved.user_id,
            channel=saved.channel.value,
            fire_at_utc=saved.fire_at_utc,
            attempts=saved.attempts,
            last_error=saved.last_error,
        )
