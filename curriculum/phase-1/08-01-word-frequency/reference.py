# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def word_frequency(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    word = ""
    for ch in text.lower() + " ":
        if "a" <= ch <= "z":
            word += ch
        elif word != "":
            counts[word] = counts.get(word, 0) + 1
            word = ""
    return counts
