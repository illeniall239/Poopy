# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def max_sum_fixed_window(values: list[int], k: int) -> int:
    if len(values) < k:
        return 0
    window = sum(values[:k])
    best = window
    for i in range(k, len(values)):
        window += values[i] - values[i - k]
        best = max(best, window)
    return best
