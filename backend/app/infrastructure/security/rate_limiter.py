from __future__ import annotations

import time
from uuid import uuid4

import redis.asyncio as aioredis

from app.core.errors import RateLimitExceededError


class RedisSlidingWindowRateLimiter:
    def __init__(self, redis_client: aioredis.Redis[bytes]) -> None:
        self._redis = redis_client

    async def check_and_consume(
        self,
        key: str,
        limit: int,
        window_seconds: int,
    ) -> None:
        now_ms = int(time.time() * 1000)
        window_start_ms = now_ms - (window_seconds * 1000)
        req_id = str(uuid4())

        pipe = self._redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start_ms)
        pipe.zcard(key)
        results = await pipe.execute()
        current_count = int(results[1])

        if current_count >= limit:
            raise RateLimitExceededError(
                f"Rate limit exceeded: maximum {limit} requests per {window_seconds}s"
            )

        pipe = self._redis.pipeline()
        pipe.zadd(key, {req_id: now_ms})
        pipe.expire(key, window_seconds + 1)
        await pipe.execute()
