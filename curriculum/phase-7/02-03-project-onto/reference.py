# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def project(a: list[float], b: list[float]) -> tuple[list[float], list[float]]:
    if len(a) != len(b):
        raise ValueError("length mismatch")
    bb = sum(y * y for y in b)
    if bb == 0:
        raise ValueError("cannot project onto the zero vector")
    scale = sum(x * y for x, y in zip(a, b)) / bb
    parallel = [scale * y for y in b]
    orthogonal = [x - p for x, p in zip(a, parallel)]
    return parallel, orthogonal
