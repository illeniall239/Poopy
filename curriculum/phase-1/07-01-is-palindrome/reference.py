# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def is_palindrome(text: str) -> bool:
    letters = ""
    for ch in text.lower():
        if "a" <= ch <= "z":
            letters += ch
    i = 0
    j = len(letters) - 1
    while i < j:
        if letters[i] != letters[j]:
            return False
        i += 1
        j -= 1
    return True
