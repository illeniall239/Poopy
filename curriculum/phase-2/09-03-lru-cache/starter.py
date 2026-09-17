class LRUCache:
    """Holds at most capacity entries; evicts the least recently used one when a new key arrives while full."""

    def __init__(self, capacity: int) -> None:
        raise NotImplementedError

    def get(self, key: int) -> int:
        """Return the value for key and mark it most recently used, or -1 if key is missing."""
        raise NotImplementedError

    def put(self, key: int, value: int) -> None:
        raise NotImplementedError
