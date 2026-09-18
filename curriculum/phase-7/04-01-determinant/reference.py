# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def determinant(a: list[list[float]]) -> float:
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("matrix must be square")
    m = [[float(x) for x in row] for row in a]
    det = 1.0
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[pivot][col]) < 1e-12:
            return 0.0
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            det = -det
        det *= m[col][col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            for c in range(col, n):
                m[r][c] -= f * m[col][c]
    return det
