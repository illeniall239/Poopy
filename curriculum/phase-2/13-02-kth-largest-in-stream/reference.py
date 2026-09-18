# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import heapq


class KthLargest:
    def __init__(self, k: int) -> None:
        self.k = k
        self.heap: list[int] = []

    def add(self, value: int) -> int | None:
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, value)
        elif value > self.heap[0]:
            heapq.heapreplace(self.heap, value)
        return self.heap[0] if len(self.heap) == self.k else None
