# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def longest_unique_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    best = 0
    left = 0
    for right, ch in enumerate(s):
        previous = last_seen.get(ch)
        if previous is not None and previous >= left:
            left = previous + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
