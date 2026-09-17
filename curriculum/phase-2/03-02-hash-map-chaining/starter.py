from typing import Generic, Optional, TypeVar

V = TypeVar("V")


class StringHashMap(Generic[V]):
    """A string-keyed hash map with 8 starting buckets, chaining, and doubling past load factor 0.75."""

    def set(self, key: str, value: V) -> None:
        """Store value under key, replacing any existing value; grow if a new key pushed the load past 0.75."""
        raise NotImplementedError

    def get(self, key: str) -> Optional[V]:
        """Return the value stored under key, or None if there is none."""
        raise NotImplementedError

    def has(self, key: str) -> bool:
        """Return whether key is stored, whatever its value."""
        raise NotImplementedError

    def delete(self, key: str) -> bool:
        """Remove key and return True, or return False if it was not stored."""
        raise NotImplementedError

    def size(self) -> int:
        """Return the number of stored keys."""
        raise NotImplementedError

    def bucket_count(self) -> int:
        """Return the current number of buckets."""
        raise NotImplementedError
