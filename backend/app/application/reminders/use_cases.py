from datetime import time
from uuid import UUID, uuid4

from app.core.errors import NotFoundError
from app.domain.entities import PushSubscription, ReminderRule, ScheduledNotification
from app.domain.repositories import UnitOfWork
from app.domain.value_objects import EventKind, NotificationChannel, NotificationStatus, QuietHours


class GetUpcomingNotificationsUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, user_id: UUID, limit: int = 50) -> list[ScheduledNotification]:
        return await self._uow.notifications.list_by_user(
            user_id, status=NotificationStatus.PENDING, limit=limit
        )


class GetUserReminderRulesUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, user_id: UUID) -> list[ReminderRule]:
        return await self._uow.reminder_rules.list_by_user(user_id)


class UpdateReminderRuleUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
        self,
        user_id: UUID,
        event_kind: EventKind,
        offsets_minutes: list[int],
        channels: list[NotificationChannel],
    ) -> ReminderRule:
        rule = await self._uow.reminder_rules.get_by_user_and_kind(user_id, event_kind)
        if rule is None:
            rule = ReminderRule(
                id=uuid4(),
                user_id=user_id,
                event_kind=event_kind,
                offsets_minutes=tuple(offsets_minutes),
                channels=tuple(channels),
            )
        else:
            rule.offsets_minutes = tuple(offsets_minutes)
            rule.channels = tuple(channels)

        return await self._uow.reminder_rules.save(rule)


class GetUserQuietHoursUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, user_id: UUID) -> QuietHours | None:
        user = await self._uow.users.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User '{user_id}' was not found")
        return user.quiet_hours


class UpdateUserQuietHoursUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
        self,
        user_id: UUID,
        start_time: time | None,
        end_time: time | None,
    ) -> QuietHours | None:
        user = await self._uow.users.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User '{user_id}' was not found")

        user.quiet_hours_start = start_time
        user.quiet_hours_end = end_time
        await self._uow.users.save(user)
        return user.quiet_hours


class RegisterPushSubscriptionUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
        self,
        user_id: UUID,
        endpoint: str,
        p256dh: str,
        auth: str,
    ) -> PushSubscription:
        sub = PushSubscription(
            id=uuid4(),
            user_id=user_id,
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth,
        )
        return await self._uow.push_subscriptions.save(sub)


class DeletePushSubscriptionUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, endpoint: str) -> None:
        await self._uow.push_subscriptions.delete_by_endpoint(endpoint)
