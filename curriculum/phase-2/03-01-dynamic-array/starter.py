from typing import Generic, TypeVar

T = TypeVar("T")


class DynamicArray(Generic[T]):
    """A growable array on fixed-capacity storage that doubles when full."""

    def size(self) -> int:
        """Return how many elements are stored."""
        raise NotImplementedError

    def capacity(self) -> int:
        """Return how many elements fit in the current storage."""
        raise NotImplementedError

    def push(self, value: T) -> None:
        """Add value at the end, doubling the storage first if it is full."""
        raise NotImplementedError

    def get(self, index: int) -> T:
        """Return the element at index; raise IndexError unless 0 <= index < size()."""
        raise NotImplementedError

    def set(self, index: int, value: T) -> None:
        """Replace the element at index; raise IndexError unless 0 <= index < size()."""
        raise NotImplementedError

    def pop(self) -> T:
        """Remove and return the last element; raise IndexError when empty."""
        raise NotImplementedError

    def to_list(self) -> list[T]:
        """Return a new list of the elements in order."""
        raise NotImplementedError
