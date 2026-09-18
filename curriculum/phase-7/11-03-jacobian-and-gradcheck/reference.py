# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import math
from collections.abc import Callable


def numeric_jacobian(f: Callable[[list[float]], list[float]], x: list[float], h: float = 1e-5) -> list[list[float]]:
    if h <= 0 or not x:
        raise ValueError("h must be positive and x non-empty")
    m = len(f(list(x)))
    jac = [[0.0] * len(x) for _ in range(m)]
    for j in range(len(x)):
        up, down = list(x), list(x)
        up[j] += h
        down[j] -= h
        fu, fd = f(up), f(down)
        for i in range(m):
            jac[i][j] = (fu[i] - fd[i]) / (2 * h)
    return jac


def gradient_check(analytic: list[float], numeric: list[float]) -> float:
    if len(analytic) != len(numeric):
        raise ValueError("length mismatch")
    diff = math.sqrt(sum((a - n) ** 2 for a, n in zip(analytic, numeric)))
    na = math.sqrt(sum(a * a for a in analytic))
    nn = math.sqrt(sum(n * n for n in numeric))
    return diff / max(na + nn, 1e-12)
