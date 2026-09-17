# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
from typing import Optional


def sorted_pair_sum(values: list[int], target: int) -> Optional[list[int]]:
    lo, hi = 0, len(values) - 1
    while lo < hi:
        total = values[lo] + values[hi]
        if total == target:
            return [values[lo], values[hi]]
        if total < target:
            lo += 1
        else:
            hi -= 1
    return None
