from typing import Optional, TypeVar

T = TypeVar("T")


def last(items: list[T]) -> Optional[T]:
    """Return the final element, or None for an empty list."""
    raise NotImplementedError


def chunk(items: list[T], size: int) -> list[list[T]]:
    """Split items into groups of `size` (the last may be shorter); raise ValueError if size < 1 or not whole."""
    raise NotImplementedError
