# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def min_shred_speed(stacks: list[int], h: int) -> int:
    lo, hi = 1, max(stacks)
    while lo < hi:
        mid = (lo + hi) // 2
        hours = sum((p + mid - 1) // mid for p in stacks)
        if hours <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo
