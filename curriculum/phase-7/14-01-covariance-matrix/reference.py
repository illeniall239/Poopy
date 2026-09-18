# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def center(rows: list[list[float]]) -> list[list[float]]:
    if not rows or any(len(r) != len(rows[0]) for r in rows):
        raise ValueError("rows must be non-empty and rectangular")
    n = len(rows)
    means = [sum(col) / n for col in zip(*rows)]
    return [[x - m for x, m in zip(row, means)] for row in rows]


def covariance_matrix(rows: list[list[float]], ddof: int = 1) -> list[list[float]]:
    centered = center(rows)
    n = len(centered)
    if n - ddof <= 0:
        raise ValueError("need more than ddof rows")
    cols = list(zip(*centered))
    d = len(cols)
    cov = [[0.0] * d for _ in range(d)]
    for i in range(d):
        for j in range(i, d):
            v = sum(a * b for a, b in zip(cols[i], cols[j])) / (n - ddof)
            cov[i][j] = cov[j][i] = v
    return cov
