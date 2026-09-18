# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def caesar_shift(text: str, shift: int) -> str:
    result = ""
    for ch in text:
        lower = ch.lower()
        index = ALPHABET.find(lower)
        if index == -1:
            result += ch
            continue
        shifted = ALPHABET[(index + shift) % 26]
        result += shifted if ch == lower else shifted.upper()
    return result
