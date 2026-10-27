from app.api.routers.auth import router as auth_router
from app.api.routers.calendar import router as calendar_router
from app.api.routers.circulars import router as circulars_router
from app.api.routers.directory import router as directory_router
from app.api.routers.metrics import router as metrics_router
from app.api.routers.reminders import router as reminders_router
from app.api.routers.tasks import router as tasks_router
from app.api.routers.timetable import router as timetable_router

__all__ = [
    "auth_router",
    "calendar_router",
    "circulars_router",
    "directory_router",
    "metrics_router",
    "reminders_router",
    "tasks_router",
    "timetable_router",
]
