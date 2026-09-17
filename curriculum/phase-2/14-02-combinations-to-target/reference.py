# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def combinations_to_target(candidates: list[int], target: int) -> list[list[int]]:
    ordered = sorted(candidates)
    result: list[list[int]] = []
    path: list[int] = []

    def explore(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(path.copy())
            return
        for i in range(start, len(ordered)):
            if ordered[i] > remaining:
                break
            path.append(ordered[i])
            explore(i, remaining - ordered[i])
            path.pop()

    explore(0, target)
    return result
