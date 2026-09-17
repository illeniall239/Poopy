# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import heapq


def merge_k_sorted(arrays: list[list[int]]) -> list[int]:
    heap = [(arr[0], a, 0) for a, arr in enumerate(arrays) if arr]
    heapq.heapify(heap)
    out = []
    while heap:
        value, a, i = heapq.heappop(heap)
        out.append(value)
        if i + 1 < len(arrays[a]):
            heapq.heappush(heap, (arrays[a][i + 1], a, i + 1))
    return out
