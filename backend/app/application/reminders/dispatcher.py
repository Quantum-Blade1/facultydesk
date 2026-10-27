from datetime import timedelta
from zoneinfo import ZoneInfo

from app.application.reminders.maths import compute_backoff_delay
from app.core.clock import Clock
from app.domain.repositories import UnitOfWork
from app.domain.value_objects import TaskStatus
from app.infrastructure.notifiers.base import NotificationPayload, Notifier


class ReminderDispatcher:
    def __init__(
        self,
        clock: Clock,
        notifier: Notifier,
        app_url: str = "http://localhost:3000",
    ) -> None:
        self._clock = clock
        self._notifier = notifier
        self._app_url = app_url.rstrip("/")

    async def dispatch_due(
        self,
        uow: UnitOfWork,
        batch_size: int = 100,
    ) -> int:
        now_utc = self._clock.now()
        async with uow:
            claimed = await uow.notifications.claim_due_batch(now_utc, limit=batch_size)
            await uow.commit()

        if not claimed:
            return 0

        dispatched_count = 0
        tz = ZoneInfo("Asia/Kolkata")

        for notif in claimed:
            async with uow:
                user = await uow.users.get_by_id(notif.user_id)
                if user is None:
                    continue

                profile = await uow.faculty_profiles.get_by_user_id(user.id)
                if notif.target_kind == "TASK":
                    task = await uow.tasks.get_by_id(notif.target_id)
                    if task is None or task.status == TaskStatus.DONE:
                        notif.cancel()
                        await uow.notifications.save(notif)
                        await uow.commit()
                        continue
                    local_dt_str = task.deadline_utc.astimezone(tz).strftime(
                        "%A, %d %b %Y at %I:%M %p"
                    )
                    payload = NotificationPayload(
                        title=f"Task Deadline: {task.title}",
                        body=f"Deadline: {local_dt_str}. Category: {task.category.value}",
                        start_time_local=local_dt_str,
                        venue=task.category.value,
                        deep_link=f"{self._app_url}/tasks",
                        event_id=task.id,
                    )
                elif notif.target_kind == "ESCALATION":
                    today_str = now_utc.astimezone(tz).strftime("%A, %d %b %Y")
                    payload = NotificationPayload(
                        title="FacultyDesk Escalation: Overdue Assigned Tasks",
                        body=(
                            "One or more documentation tasks assigned to faculty "
                            "are overdue by 24h or more."
                        ),
                        start_time_local=today_str,
                        venue="Departmental Tasks",
                        deep_link=f"{self._app_url}/tasks/dashboard",
                        event_id=notif.target_id,
                    )
                else:
                    event = await uow.events.get_by_id(notif.target_id)
                    if event is None:
                        continue

                    local_dt_str = event.start_utc.astimezone(tz).strftime(
                        "%A, %d %b %Y at %I:%M %p"
                    )
                    payload = NotificationPayload(
                        title=event.title,
                        body=f"{event.location} at {local_dt_str}",
                        start_time_local=local_dt_str,
                        venue=event.location,
                        deep_link=f"{self._app_url}/calendar?event={event.id}",
                        event_id=event.id,
                    )

                try:
                    await self._notifier.send(
                        notification=notif,
                        payload=payload,
                        recipient_user=user,
                        recipient_profile=profile,
                        uow=uow,
                    )
                    notif.mark_sent(delivered_at=self._clock.now())
                    await uow.notifications.save(notif)
                    await uow.commit()
                    dispatched_count += 1
                except Exception as exc:
                    delay_seconds = compute_backoff_delay(notif.attempts)
                    if notif.attempts < notif.max_attempts:
                        notif.retry()
                        notif.fire_at_utc = self._clock.now() + timedelta(seconds=delay_seconds)
                        notif.last_error = str(exc)
                    else:
                        notif.mark_failed(str(exc))
                    await uow.notifications.save(notif)
                    await uow.commit()

        return dispatched_count

    async def recover_stale_sending(
        self,
        uow: UnitOfWork,
        stale_minutes: int = 5,
    ) -> int:
        cutoff_utc = self._clock.now() - timedelta(minutes=stale_minutes)
        async with uow:
            recovered = await uow.notifications.recover_stale_sending(cutoff_utc)
            await uow.commit()
            return recovered
