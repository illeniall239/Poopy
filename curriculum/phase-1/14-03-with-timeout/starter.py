from typing import Awaitable


async def sleep(ms: float) -> None:
    """Pause for ms milliseconds without blocking the event loop."""
    raise NotImplementedError


async def with_timeout(awaitable: Awaitable[str], ms: float) -> str:
    """Return the awaitable's result, or raise TimeoutError("Timed out after <ms>ms") if it takes longer than ms."""
    raise NotImplementedError
