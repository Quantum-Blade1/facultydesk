from app.domain.entities import FacultyProfile, ScheduledNotification, User
from app.domain.repositories import UnitOfWork
from app.domain.value_objects import NotificationChannel
from app.infrastructure.notifiers.base import NotificationPayload, Notifier
from app.infrastructure.notifiers.email import EmailNotifier
from app.infrastructure.notifiers.web_push import WebPushNotifier


class CompositeNotifier(Notifier):
    def __init__(
        self,
        email_notifier: Notifier,
        push_notifier: Notifier,
    ) -> None:
        self._email = email_notifier
        self._push = push_notifier

    async def send(
        self,
        notification: ScheduledNotification,
        payload: NotificationPayload,
        recipient_user: User,
        recipient_profile: FacultyProfile | None,
        uow: UnitOfWork,
    ) -> None:
        if notification.channel == NotificationChannel.EMAIL:
            await self._email.send(
                notification, payload, recipient_user, recipient_profile, uow
            )
        elif notification.channel == NotificationChannel.PUSH:
            await self._push.send(
                notification, payload, recipient_user, recipient_profile, uow
            )


__all__ = [
    "CompositeNotifier",
    "EmailNotifier",
    "NotificationPayload",
    "Notifier",
    "WebPushNotifier",
]
