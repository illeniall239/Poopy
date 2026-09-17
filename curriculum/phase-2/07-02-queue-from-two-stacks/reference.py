# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class TwoStackQueue(Generic[T]):
    def __init__(self) -> None:
        self._incoming: list[T] = []
        self._outgoing: list[T] = []

    def enqueue(self, value: T) -> None:
        self._incoming.append(value)

    def dequeue(self) -> Optional[T]:
        self._refill()
        return self._outgoing.pop() if self._outgoing else None

    def peek(self) -> Optional[T]:
        self._refill()
        return self._outgoing[-1] if self._outgoing else None

    def size(self) -> int:
        return len(self._incoming) + len(self._outgoing)

    def _refill(self) -> None:
        if not self._outgoing:
            while self._incoming:
                self._outgoing.append(self._incoming.pop())
