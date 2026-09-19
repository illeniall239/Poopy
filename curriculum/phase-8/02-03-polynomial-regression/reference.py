# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def solve(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(a)
    if any(len(row) != n for row in a) or len(b) != n:
        raise ValueError("shape mismatch")
    m = [[float(x) for x in row] + [float(bi)] for row, bi in zip(a, b)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[pivot][col]) < 1e-12:
            raise ValueError("singular matrix")
        m[col], m[pivot] = m[pivot], m[col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            for c in range(col, n + 1):
                m[r][c] -= f * m[col][c]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(m[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (m[i][n] - s) / m[i][i]
    return x


def polynomial_features(xs: list[float], degree: int) -> list[list[float]]:
    if degree < 0:
        raise ValueError("degree must be >= 0")
    return [[float(x) ** p for p in range(degree + 1)] for x in xs]


def fit_polynomial(xs: list[float], ys: list[float], degree: int) -> list[float]:
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    X = polynomial_features(xs, degree)
    k = degree + 1
    xtx = [[sum(row[i] * row[j] for row in X) for j in range(k)] for i in range(k)]
    xty = [sum(row[i] * y for row, y in zip(X, ys)) for i in range(k)]
    return solve(xtx, xty)
