import hashlib
import random
from datetime import UTC, datetime, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from app.domain.value_objects import NotificationChannel, QuietHours


def compute_fire_time(start_utc: datetime, offset_minutes: int) -> datetime:
    return start_utc - timedelta(minutes=offset_minutes)


def compute_idempotency_key(
    target_id: UUID,
    user_id: UUID,
    offset_minutes: int,
    channel: NotificationChannel,
) -> str:
    raw = f"{target_id}:{user_id}:{offset_minutes}:{channel.value}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def compute_backoff_delay(
    attempt: int,
    base_seconds: float = 30.0,
    cap_seconds: float = 1800.0,
) -> float:
    ceiling = min(cap_seconds, base_seconds * (2**attempt))
    return random.uniform(0.0, ceiling)


def adjust_for_quiet_hours(
    fire_utc: datetime,
    event_start_utc: datetime,
    quiet_hours: QuietHours | None,
    timezone_str: str = "Asia/Kolkata",
) -> datetime:
    if quiet_hours is None or quiet_hours.start_time == quiet_hours.end_time:
        return fire_utc

    tz = ZoneInfo(timezone_str)
    local_fire = fire_utc.astimezone(tz)
    local_time = local_fire.time()

    if not quiet_hours.covers(local_time):
        return fire_utc

    local_date = local_fire.date()
    if not quiet_hours.crosses_midnight:
        window_end_local = datetime.combine(local_date, quiet_hours.end_time, tzinfo=tz)
    else:
        if local_time >= quiet_hours.start_time:
            next_day = local_date + timedelta(days=1)
            window_end_local = datetime.combine(next_day, quiet_hours.end_time, tzinfo=tz)
        else:
            window_end_local = datetime.combine(local_date, quiet_hours.end_time, tzinfo=tz)

    window_end_utc = window_end_local.astimezone(UTC)
    if event_start_utc <= window_end_utc:
        return fire_utc

    return window_end_utc
