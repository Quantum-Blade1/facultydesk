import math
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo


def compute_priority_score(
    importance: int,
    deadline_utc: datetime,
    now_utc: datetime,
    is_completed: bool = False,
) -> float:
    if is_completed:
        return -1.0

    if now_utc.tzinfo is None or deadline_utc.tzinfo is None:
        raise ValueError("Datetimes must be timezone-aware")

    diff_seconds = (deadline_utc - now_utc).total_seconds()

    if diff_seconds <= 0:
        overdue_days = abs(diff_seconds) / 86400.0
        capped_days = min(overdue_days, 7.0)
        return round(1.0 + (capped_days / 7.0), 4)

    h = diff_seconds / 3600.0
    w_i = 0.4
    w_u = 0.6
    tau = 48.0

    importance_component = w_i * ((importance - 1) / 4.0)
    urgency_component = w_u * math.exp(-h / tau)

    return round(importance_component + urgency_component, 4)


def compute_lead_alert_times(
    deadline_utc: datetime,
    created_at_utc: datetime,
) -> list[datetime]:
    offsets_hours = [72, 24, 2]
    planned: list[datetime] = []
    for h in offsets_hours:
        lead_time = deadline_utc - timedelta(hours=h)
        if lead_time > created_at_utc:
            planned.append(lead_time)
    return sorted(planned)


def compute_overdue_alert_times(
    deadline_utc: datetime,
    until_date: date,
    tz_name: str = "Asia/Kolkata",
) -> list[datetime]:
    tz = ZoneInfo(tz_name)
    deadline_local = deadline_utc.astimezone(tz)
    deadline_date = deadline_local.date()

    alerts: list[datetime] = []
    curr = deadline_date + timedelta(days=1)
    while curr <= until_date:
        alert_local = datetime.combine(curr, time(9, 0), tzinfo=tz)
        alerts.append(alert_local.astimezone(UTC))
        curr += timedelta(days=1)
    return alerts


def compute_completion_rate(total_tasks: int, completed_tasks: int) -> float:
    if total_tasks <= 0:
        return 100.0
    return round((completed_tasks / total_tasks) * 100.0, 2)
