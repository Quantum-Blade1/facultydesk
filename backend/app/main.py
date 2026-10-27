from contextlib import asynccontextmanager
from typing import Any

import redis.asyncio as aioredis
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from minio import Minio
from sqlalchemy import text

from app.api.routers import (
    auth_router,
    calendar_router,
    circulars_router,
    directory_router,
    reminders_router,
    tasks_router,
    timetable_router,
)
from app.core.config import get_settings
from app.core.db import engine
from app.core.errors import FacultyDeskError
from app.core.logging import RequestIdMiddleware, configure_logging

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    configure_logging()
    yield


app = FastAPI(
    title="FacultyDesk API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIdMiddleware)

app.include_router(auth_router, prefix="/api")
app.include_router(directory_router, prefix="/api")
app.include_router(timetable_router, prefix="/api")
app.include_router(calendar_router, prefix="/api")
app.include_router(reminders_router, prefix="/api")
app.include_router(circulars_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")




@app.exception_handler(FacultyDeskError)
async def domain_exception_handler(request: Request, exc: FacultyDeskError) -> JSONResponse:
    status_code = status.HTTP_400_BAD_REQUEST
    if exc.code == "NOT_FOUND":
        status_code = status.HTTP_404_NOT_FOUND
    elif exc.code == "UNAUTHORIZED":
        status_code = status.HTTP_401_UNAUTHORIZED
    elif exc.code == "FORBIDDEN":
        status_code = status.HTTP_403_FORBIDDEN
    elif exc.code == "CONFLICT":
        status_code = status.HTTP_409_CONFLICT
    elif exc.code == "VALIDATION_ERROR" or exc.code == "INVALID_TRANSITION":
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif exc.code == "RATE_LIMIT_EXCEEDED":
        status_code = status.HTTP_429_TOO_MANY_REQUESTS

    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Process liveness probe."""
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> JSONResponse:
    """Readiness probe checking Postgres, Redis, and MinIO."""
    failing: list[str] = []

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        failing.append("postgres")

    try:
        redis_client = aioredis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        await redis_client.close()
    except Exception:
        failing.append("redis")

    try:
        minio_client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
            failing.append("minio")
    except Exception:
        failing.append("minio")

    if failing:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "failing": failing},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "ready"},
    )
