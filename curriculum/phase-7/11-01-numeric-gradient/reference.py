# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
from collections.abc import Callable


def numeric_gradient(f: Callable[[list[float]], float], params: list[float], h: float = 1e-5) -> list[float]:
    if h <= 0:
        raise ValueError("h must be positive")
    grad = []
    for i in range(len(params)):
        up = list(params)
        down = list(params)
        up[i] += h
        down[i] -= h
        grad.append((f(up) - f(down)) / (2 * h))
    return grad
