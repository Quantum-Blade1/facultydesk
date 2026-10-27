import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from pywebpush import WebPushException, webpush

from app.domain.entities import FacultyProfile, ScheduledNotification, User
from app.domain.repositories import UnitOfWork
from app.infrastructure.notifiers.base import NotificationPayload, Notifier


class WebPushNotifier(Notifier):
    def __init__(
        self,
        vapid_private_key: str,
        vapid_claims_email: str,
    ) -> None:
        self._vapid_private_key = vapid_private_key
        self._vapid_claims_email = vapid_claims_email
        self._executor = ThreadPoolExecutor(max_workers=4)

    async def send(
        self,
        notification: ScheduledNotification,
        payload: NotificationPayload,
        recipient_user: User,
        recipient_profile: FacultyProfile | None,
        uow: UnitOfWork,
    ) -> None:
        if not self._vapid_private_key:
            return

        subscriptions = await uow.push_subscriptions.list_by_user(recipient_user.id)
        if not subscriptions:
            return

        message_data = json.dumps(
            {
                "title": payload.title,
                "body": f"{payload.venue} at {payload.start_time_local}",
                "url": payload.deep_link,
                "data": {
                    "eventId": str(payload.event_id),
                    "venue": payload.venue,
                    "startTime": payload.start_time_local,
                },
            }
        )

        loop = asyncio.get_running_loop()
        endpoints_to_delete: list[str] = []

        for sub in subscriptions:
            sub_info = {
                "endpoint": sub.endpoint,
                "keys": {
                    "p256dh": sub.p256dh,
                    "auth": sub.auth,
                },
            }
            try:
                await loop.run_in_executor(
                    self._executor,
                    self._sync_webpush,
                    sub_info,
                    message_data,
                )
            except WebPushException as exc:
                resp = exc.response
                status_code = getattr(resp, "status_code", None) if resp is not None else None
                if status_code in (404, 410):
                    endpoints_to_delete.append(sub.endpoint)
                else:
                    raise

        for endpoint in endpoints_to_delete:
            await uow.push_subscriptions.delete_by_endpoint(endpoint)

    def _sync_webpush(self, sub_info: dict[str, Any], data: str) -> None:
        webpush(
            subscription_info=sub_info,
            data=data,
            vapid_private_key=self._vapid_private_key,
            vapid_claims={"sub": f"mailto:{self._vapid_claims_email}"},
            timeout=10,
        )
