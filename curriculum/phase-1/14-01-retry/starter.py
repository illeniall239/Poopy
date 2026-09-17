from typing import Awaitable, Callable


async def retry(task: Callable[[], Awaitable[str]], max_attempts: int, delay_ms: float = 0) -> str:
    """Await task() up to max_attempts times, waiting delay_ms between attempts; re-raise the last error if all fail."""
    raise NotImplementedError
