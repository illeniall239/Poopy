# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def climb_ways(n: int) -> int:
    two_below, one_below = 1, 1
    for _ in range(2, n + 1):
        two_below, one_below = one_below, one_below + two_below
    return one_below
