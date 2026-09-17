class MinHeap:
    """A min-heap stored in a list. Write it yourself: no heapq."""

    def __init__(self, values: list[int] | None = None) -> None:
        """Start with all of these values. Must not change the list passed in."""
        raise NotImplementedError

    def push(self, value: int) -> None:
        raise NotImplementedError

    def pop(self) -> int | None:
        """Remove and return the smallest value, or None if empty."""
        raise NotImplementedError

    def peek(self) -> int | None:
        """Return the smallest value without removing it, or None if empty."""
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError
