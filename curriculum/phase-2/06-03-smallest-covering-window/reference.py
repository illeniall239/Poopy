# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
from collections import Counter


def smallest_covering_window(s: str, t: str) -> str:
    if not t or len(s) < len(t):
        return ""
    need = Counter(t)
    missing = len(need)
    have: dict[str, int] = {}
    best_start, best_length = 0, None
    left = 0
    for right, ch in enumerate(s):
        if ch not in need:
            continue
        have[ch] = have.get(ch, 0) + 1
        if have[ch] == need[ch]:
            missing -= 1
        while missing == 0:
            if best_length is None or right - left + 1 < best_length:
                best_start, best_length = left, right - left + 1
            out = s[left]
            left += 1
            if out in need:
                have[out] -= 1
                if have[out] < need[out]:
                    missing += 1
    return "" if best_length is None else s[best_start:best_start + best_length]
