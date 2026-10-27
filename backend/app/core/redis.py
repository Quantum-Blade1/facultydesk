from __future__ import annotations

from functools import lru_cache

import redis.asyncio as aioredis

from app.core.config import get_settings


@lru_cache
def get_redis_client() -> aioredis.Redis[bytes]:
    settings = get_settings()
    return aioredis.from_url(settings.REDIS_URL)
