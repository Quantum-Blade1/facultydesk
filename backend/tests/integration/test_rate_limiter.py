import asyncio
from uuid import uuid4

import pytest

from app.core.errors import RateLimitExceededError
from app.core.redis import get_redis_client
from app.infrastructure.security.rate_limiter import RedisSlidingWindowRateLimiter


@pytest.mark.asyncio
async def test_sliding_window_rate_limiter() -> None:
    redis = get_redis_client()
    limiter = RedisSlidingWindowRateLimiter(redis)
    test_key = f"test_ratelimit:{uuid4().hex}"

    for _ in range(3):
        await limiter.check_and_consume(test_key, limit=3, window_seconds=2)

    with pytest.raises(RateLimitExceededError):
        await limiter.check_and_consume(test_key, limit=3, window_seconds=2)

    await asyncio.sleep(2.1)

    await limiter.check_and_consume(test_key, limit=3, window_seconds=2)
