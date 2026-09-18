# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class DynamicArray(Generic[T]):
    def __init__(self) -> None:
        self._storage: list[Optional[T]] = [None]
        self._count = 0

    def size(self) -> int:
        return self._count

    def capacity(self) -> int:
        return len(self._storage)

    def push(self, value: T) -> None:
        if self._count == len(self._storage):
            bigger: list[Optional[T]] = [None] * (len(self._storage) * 2)
            for i in range(self._count):
                bigger[i] = self._storage[i]
            self._storage = bigger
        self._storage[self._count] = value
        self._count += 1

    def get(self, index: int) -> T:
        self._check_index(index)
        return self._storage[index]  # type: ignore[return-value]

    def set(self, index: int, value: T) -> None:
        self._check_index(index)
        self._storage[index] = value

    def pop(self) -> T:
        if self._count == 0:
            raise IndexError("pop from empty DynamicArray")
        self._count -= 1
        value = self._storage[self._count]
        self._storage[self._count] = None
        return value  # type: ignore[return-value]

    def to_list(self) -> list[T]:
        return [self._storage[i] for i in range(self._count)]  # type: ignore[misc]

    def _check_index(self, index: int) -> None:
        if index < 0 or index >= self._count:
            raise IndexError(f"index {index} out of range")
