# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def top_k_frequent(values: list[int], k: int) -> list[int]:
    counts: dict[int, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1

    # by_count[c] holds the values seen exactly c times, in first-appearance order (dicts keep insertion order).
    by_count: list[list[int]] = [[] for _ in range(len(values) + 1)]
    for value, count in counts.items():
        by_count[count].append(value)

    result: list[int] = []
    for count in range(len(values), 0, -1):
        for value in by_count[count]:
            if len(result) == k:
                return result
            result.append(value)
    return result
