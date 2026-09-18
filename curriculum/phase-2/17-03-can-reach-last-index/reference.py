# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.


def can_reach_last_index(jumps: list[int]) -> bool:
    farthest = 0
    for i, jump in enumerate(jumps):
        if i > farthest:
            break
        farthest = max(farthest, i + jump)
    return farthest >= len(jumps) - 1
