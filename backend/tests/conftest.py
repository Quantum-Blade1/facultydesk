from collections.abc import AsyncGenerator

import pytest

from app.core.db import engine


@pytest.fixture(autouse=True)
async def cleanup_db_connections() -> AsyncGenerator[None, None]:
    yield
    await engine.dispose()
