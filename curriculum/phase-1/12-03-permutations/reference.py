# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def permutations(s: str) -> list[str]:
    if len(s) == 0:
        return [""]
    results: set[str] = set()
    for i in range(len(s)):
        rest = s[:i] + s[i + 1 :]
        for tail in permutations(rest):
            results.add(s[i] + tail)
    return sorted(results)
