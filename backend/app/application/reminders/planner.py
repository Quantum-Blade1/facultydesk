from uuid import UUID

from app.application.reminders.maths import (
    adjust_for_quiet_hours,
    compute_fire_time,
    compute_idempotency_key,
)
from app.core.clock import Clock
from app.domain.entities import Event, ScheduledNotification
from app.domain.repositories import UnitOfWork
from app.domain.value_objects import EventKind, NotificationChannel, NotificationStatus

DEFAULT_OFFSETS: dict[EventKind, tuple[int, ...]] = {
    EventKind.CLASS: (15,),
    EventKind.MEETING: (1440, 60, 10),
    EventKind.DEADLINE: (2880, 1440, 120),
    EventKind.CUSTOM: (60, 15),
}

DEFAULT_CHANNELS: tuple[NotificationChannel, ...] = (
    NotificationChannel.EMAIL,
    NotificationChannel.PUSH,
)


class ReminderPlanner:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock

    async def plan_event_reminders(
        self,
        event: Event,
        uow: UnitOfWork,
    ) -> list[ScheduledNotification]:
        planned: list[ScheduledNotification] = []
        now_utc = self._clock.now()
        valid_keys: set[str] = set()

        for attendee in event.attendees:
            faculty = await uow.faculty_profiles.get_by_id(attendee.faculty_id)
            if faculty is None:
                continue

            user = await uow.users.get_by_id(faculty.user_id)
            if user is None or not user.is_active:
                continue

            rule = await uow.reminder_rules.get_by_user_and_kind(user.id, event.kind)
            offsets = rule.offsets_minutes if rule else DEFAULT_OFFSETS.get(event.kind, (15,))
            channels = rule.channels if rule else DEFAULT_CHANNELS

            for offset in offsets:
                f_time = compute_fire_time(event.start_utc, offset)
                if f_time <= now_utc:
                    continue

                f_adjusted = adjust_for_quiet_hours(f_time, event.start_utc, user.quiet_hours)
                for channel in channels:
                    key = compute_idempotency_key(event.id, user.id, offset, channel)
                    valid_keys.add(key)
                    existing = await uow.notifications.get_by_idempotency_key(key)

                    if existing is None:
                        notif = ScheduledNotification(
                            target_id=event.id,
                            target_kind="EVENT",
                            user_id=user.id,
                            channel=channel,
                            fire_at_utc=f_adjusted,
                            idempotency_key=key,
                            status=NotificationStatus.PENDING,
                        )
                        saved = await uow.notifications.save(notif)
                        planned.append(saved)
                    elif existing.status == NotificationStatus.PENDING:
                        existing.fire_at_utc = f_adjusted
                        saved = await uow.notifications.save(existing)
                        planned.append(saved)

        existing_target_notifs = await uow.notifications.list_by_target(event.id)
        for notif in existing_target_notifs:
            is_pending = notif.status == NotificationStatus.PENDING
            if is_pending and notif.idempotency_key not in valid_keys:
                notif.cancel()
                await uow.notifications.save(notif)

        return planned

    async def handle_event_rescheduled(
        self,
        event: Event,
        uow: UnitOfWork,
    ) -> list[ScheduledNotification]:
        return await self.plan_event_reminders(event, uow)

    async def handle_event_cancelled(
        self,
        event_id: UUID,
        uow: UnitOfWork,
    ) -> int:
        return await uow.notifications.cancel_pending_by_target(event_id)
