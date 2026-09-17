from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class TwoStackQueue(Generic[T]):
    """A FIFO queue stored in two lists used only as stacks (append, pop, len, [-1])."""

    def enqueue(self, value: T) -> None:
        raise NotImplementedError

    def dequeue(self) -> Optional[T]:
        """Remove and return the front value, or None when the queue is empty."""
        raise NotImplementedError

    def peek(self) -> Optional[T]:
        """Return the front value without removing it, or None when the queue is empty."""
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError
