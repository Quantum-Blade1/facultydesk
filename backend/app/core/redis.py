from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING, Any

import redis.asyncio as aioredis

from app.core.config import get_settings

if TYPE_CHECKING:
    RedisClient = aioredis.Redis[bytes]
else:
    RedisClient = Any


@lru_cache
def get_redis_client() -> RedisClient:
    settings = get_settings()
    return aioredis.from_url(settings.REDIS_URL)
