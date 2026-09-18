# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def matrix_rank(a: list[list[float]], tol: float = 1e-9) -> int:
    m = [[float(x) for x in row] for row in a]
    rows, cols = len(m), len(m[0]) if m else 0
    r = 0
    for c in range(cols):
        if r == rows:
            break
        pivot = max(range(r, rows), key=lambda i: abs(m[i][c]))
        if abs(m[pivot][c]) <= tol:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        for i in range(r + 1, rows):
            f = m[i][c] / m[r][c]
            for j in range(c, cols):
                m[i][j] -= f * m[r][j]
        r += 1
    return r


def is_singular(a: list[list[float]], tol: float = 1e-9) -> bool:
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("matrix must be square")
    return matrix_rank(a, tol) < n
