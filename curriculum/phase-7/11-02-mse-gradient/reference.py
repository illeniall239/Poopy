# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def _check(xs: list[float], ys: list[float]) -> None:
    if len(xs) != len(ys) or not xs:
        raise ValueError("xs and ys must be non-empty and the same length")


def mse(w: float, b: float, xs: list[float], ys: list[float]) -> float:
    _check(xs, ys)
    return sum((w * x + b - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


def mse_gradient(w: float, b: float, xs: list[float], ys: list[float]) -> tuple[float, float]:
    _check(xs, ys)
    n = len(xs)
    dw = db = 0.0
    for x, y in zip(xs, ys):
        r = w * x + b - y
        dw += r * x
        db += r
    return 2 * dw / n, 2 * db / n
