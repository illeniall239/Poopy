# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def range_sums(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    # prefix[k] is the sum of the first k values.
    prefix = [0] * (len(values) + 1)
    for k, value in enumerate(values):
        prefix[k + 1] = prefix[k] + value
    return [prefix[j + 1] - prefix[i] for i, j in queries]
