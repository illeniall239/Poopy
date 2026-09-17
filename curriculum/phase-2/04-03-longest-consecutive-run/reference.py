# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def longest_consecutive_run(values: list[int]) -> int:
    present = set(values)
    best = 0
    for start in present:
        if start - 1 in present:
            continue
        length = 1
        while start + length in present:
            length += 1
        best = max(best, length)
    return best
