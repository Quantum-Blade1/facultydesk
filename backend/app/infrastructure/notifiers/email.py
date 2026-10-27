from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.domain.entities import FacultyProfile, ScheduledNotification, User
from app.domain.repositories import UnitOfWork
from app.infrastructure.notifiers.base import NotificationPayload, Notifier


class EmailNotifier(Notifier):
    def __init__(
        self,
        hostname: str,
        port: int,
        sender: str,
        username: str = "",
        password: str = "",
        use_tls: bool = False,
    ) -> None:
        self._hostname = hostname
        self._port = port
        self._sender = sender
        self._username = username
        self._password = password
        self._use_tls = use_tls

    async def send(
        self,
        notification: ScheduledNotification,
        payload: NotificationPayload,
        recipient_user: User,
        recipient_profile: FacultyProfile | None,
        uow: UnitOfWork,
    ) -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"FacultyDesk Reminder: {payload.title}"
        msg["From"] = self._sender
        msg["To"] = recipient_user.email

        recipient_name = recipient_profile.full_name if recipient_profile else recipient_user.email
        text_body = (
            f"Hello {recipient_name},\n\n"
            f"This is a reminder for your upcoming event:\n"
            f"Title: {payload.title}\n"
            f"Time: {payload.start_time_local}\n"
            f"Venue: {payload.venue}\n\n"
            f"View in FacultyDesk: {payload.deep_link}\n"
        )
        body_style = "font-family: sans-serif; line-height: 1.5; color: #1e293b; padding: 20px;"
        box_style = (
            "background-color: #f8fafc; border: 1px solid #e2e8f0; "
            "border-radius: 8px; padding: 16px; margin: 16px 0;"
        )
        btn_style = (
            "display: inline-block; background-color: #0284c7; color: #ffffff; "
            "text-decoration: none; padding: 10px 18px; border-radius: 6px; font-weight: 500;"
        )
        footer_style = "font-size: 12px; color: #64748b;"
        html_body = (
            f"<!DOCTYPE html>"
            f"<html>"
            f"<body style='{body_style}'>"
            f"<h2 style='color: #0f172a; margin-bottom: 12px;'>Upcoming Event Reminder</h2>"
            f"<p>Hello <strong>{recipient_name}</strong>,</p>"
            f"<div style='{box_style}'>"
            f"<h3 style='margin-top: 0; color: #0284c7;'>{payload.title}</h3>"
            f"<p style='margin: 4px 0;'><strong>Time:</strong> {payload.start_time_local}</p>"
            f"<p style='margin: 4px 0;'><strong>Venue:</strong> {payload.venue}</p>"
            f"</div>"
            f"<p><a href='{payload.deep_link}' style='{btn_style}'>View in FacultyDesk</a></p>"
            f"<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 24px 0;'/>"
            f"<p style='{footer_style}'>"
            f"Delivered exactly-once by FacultyDesk Notification Engine."
            f"</p>"
            f"</body>"
            f"</html>"
        )
        msg.attach(MIMEText(text_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        await aiosmtplib.send(
            msg,
            hostname=self._hostname,
            port=self._port,
            username=self._username if self._username else None,
            password=self._password if self._password else None,
            start_tls=self._use_tls,
        )
