# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import asyncio
from typing import Awaitable, Callable


async def retry(task: Callable[[], Awaitable[str]], max_attempts: int, delay_ms: float = 0) -> str:
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return await task()
        except Exception as error:
            last_error = error
            if attempt < max_attempts:
                await asyncio.sleep(delay_ms / 1000)
    raise last_error
