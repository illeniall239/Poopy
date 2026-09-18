# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
class MinHeap:
    def __init__(self, values: list[int] | None = None) -> None:
        self.items = list(values or [])
        for i in range(len(self.items) // 2 - 1, -1, -1):
            self._sift_down(i)

    def push(self, value: int) -> None:
        a = self.items
        a.append(value)
        i = len(a) - 1
        while i > 0:
            parent = (i - 1) // 2
            if a[parent] <= a[i]:
                break
            a[parent], a[i] = a[i], a[parent]
            i = parent

    def pop(self) -> int | None:
        a = self.items
        if not a:
            return None
        top = a[0]
        last = a.pop()
        if a:
            a[0] = last
            self._sift_down(0)
        return top

    def peek(self) -> int | None:
        return self.items[0] if self.items else None

    def size(self) -> int:
        return len(self.items)

    def _sift_down(self, i: int) -> None:
        a = self.items
        n = len(a)
        while True:
            l, r = 2 * i + 1, 2 * i + 2
            smallest = i
            if l < n and a[l] < a[smallest]:
                smallest = l
            if r < n and a[r] < a[smallest]:
                smallest = r
            if smallest == i:
                return
            a[smallest], a[i] = a[i], a[smallest]
            i = smallest
