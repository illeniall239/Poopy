# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def first_unique_index(text: str) -> int:
    counts: dict[str, int] = {}
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
    for i in range(len(text)):
        if counts[text[i]] == 1:
            return i
    return -1
