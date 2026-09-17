# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
from typing import Optional, TypeVar

T = TypeVar("T")


def last(items: list[T]) -> Optional[T]:
    return items[-1] if items else None


def chunk(items: list[T], size: int) -> list[list[T]]:
    if not isinstance(size, int) or size < 1:
        raise ValueError(f"size must be a whole number of at least 1, got {size}")
    return [items[start : start + size] for start in range(0, len(items), size)]
