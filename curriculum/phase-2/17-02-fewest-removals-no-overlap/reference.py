# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.


def fewest_removals(intervals: list[list[int]]) -> int:
    removed = 0
    last_end = float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if start < last_end:
            removed += 1
        else:
            last_end = end
    return removed
