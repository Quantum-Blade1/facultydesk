from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from app.domain.entities import FacultyProfile, ScheduledNotification, User
from app.domain.repositories import UnitOfWork


@dataclass(frozen=True)
class NotificationPayload:
    title: str
    body: str
    start_time_local: str
    venue: str
    deep_link: str
    event_id: UUID


class Notifier(ABC):
    @abstractmethod
    async def send(
        self,
        notification: ScheduledNotification,
        payload: NotificationPayload,
        recipient_user: User,
        recipient_profile: FacultyProfile | None,
        uow: UnitOfWork,
    ) -> None:
        """Send notification via this channel. Raise on failure to trigger retry backoff."""
