# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import asyncio
from typing import Awaitable


async def sleep(ms: float) -> None:
    await asyncio.sleep(ms / 1000)


async def with_timeout(awaitable: Awaitable[str], ms: float) -> str:
    if ms < 0:
        raise ValueError("ms must not be negative")
    try:
        return await asyncio.wait_for(awaitable, ms / 1000)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Timed out after {ms}ms") from None
