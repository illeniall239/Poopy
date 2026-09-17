class KthLargest:
    """Tracks the k-th largest number added so far. heapq is allowed."""

    def __init__(self, k: int) -> None:
        raise NotImplementedError

    def add(self, value: int) -> int | None:
        """Record value; return the k-th largest so far, or None if fewer than k numbers."""
        raise NotImplementedError
