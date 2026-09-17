# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def permutations(s: str) -> list[str]:
    if len(s) == 0:
        return [""]
    results: set[str] = set()
    for i in range(len(s)):
        rest = s[:i] + s[i + 1 :]
        for tail in permutations(rest):
            results.add(s[i] + tail)
    return sorted(results)
