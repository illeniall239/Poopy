# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).


def can_reach_last_index(jumps: list[int]) -> bool:
    farthest = 0
    for i, jump in enumerate(jumps):
        if i > farthest:
            break
        farthest = max(farthest, i + jump)
    return farthest >= len(jumps) - 1
