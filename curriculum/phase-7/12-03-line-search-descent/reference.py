# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
from collections.abc import Callable


def backtracking_step(
    f: Callable[[list[float]], float],
    x: list[float],
    fx: float,
    g: list[float],
    alpha0: float = 1.0,
    beta: float = 0.5,
    c: float = 1e-4,
    max_halvings: int = 60,
) -> float:
    if alpha0 <= 0 or not 0 < beta < 1 or not 0 < c < 1:
        raise ValueError("alpha0 > 0, 0 < beta < 1 and 0 < c < 1 required")
    gg = sum(gi * gi for gi in g)
    alpha = alpha0
    for _ in range(max_halvings):
        trial = [xi - alpha * gi for xi, gi in zip(x, g)]
        if f(trial) <= fx - c * alpha * gg:
            return alpha
        alpha *= beta
    return alpha


def line_search_descent(
    f: Callable[[list[float]], float],
    grad_f: Callable[[list[float]], list[float]],
    x0: list[float],
    tol: float = 1e-6,
    max_steps: int = 1000,
) -> tuple[list[float], int]:
    x = list(x0)
    for step in range(max_steps):
        g = grad_f(x)
        if math.sqrt(sum(gi * gi for gi in g)) < tol:
            return x, step
        alpha = backtracking_step(f, x, f(x), g)
        x = [xi - alpha * gi for xi, gi in zip(x, g)]
    return x, max_steps
