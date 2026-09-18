# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Generic, Optional, TypeVar

V = TypeVar("V")


class StringHashMap(Generic[V]):
    def __init__(self) -> None:
        self._buckets: list[list[list]] = [[] for _ in range(8)]
        self._count = 0

    @staticmethod
    def _bucket_for(key: str, buckets: list[list[list]]) -> list[list]:
        return buckets[hash(key) % len(buckets)]

    def set(self, key: str, value: V) -> None:
        bucket = self._bucket_for(key, self._buckets)
        for entry in bucket:
            if entry[0] == key:
                entry[1] = value
                return
        bucket.append([key, value])
        self._count += 1
        if self._count / len(self._buckets) > 0.75:
            self._resize()

    def get(self, key: str) -> Optional[V]:
        for k, v in self._bucket_for(key, self._buckets):
            if k == key:
                return v
        return None

    def has(self, key: str) -> bool:
        return any(k == key for k, _ in self._bucket_for(key, self._buckets))

    def delete(self, key: str) -> bool:
        bucket = self._bucket_for(key, self._buckets)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = bucket[-1]
                bucket.pop()
                self._count -= 1
                return True
        return False

    def size(self) -> int:
        return self._count

    def bucket_count(self) -> int:
        return len(self._buckets)

    def _resize(self) -> None:
        bigger: list[list[list]] = [[] for _ in range(len(self._buckets) * 2)]
        for bucket in self._buckets:
            for entry in bucket:
                self._bucket_for(entry[0], bigger).append(entry)
        self._buckets = bigger
