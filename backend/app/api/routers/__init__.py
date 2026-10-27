from app.api.routers.auth import router as auth_router
from app.api.routers.directory import router as directory_router
from app.api.routers.timetable import router as timetable_router

__all__ = ["auth_router", "directory_router", "timetable_router"]
