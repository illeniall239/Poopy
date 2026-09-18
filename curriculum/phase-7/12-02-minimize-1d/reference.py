# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
from collections.abc import Callable


def minimize_1d(
    f: Callable[[float], float],
    x0: float,
    lr: float,
    tol: float = 1e-8,
    max_steps: int = 10_000,
    h: float = 1e-5,
) -> tuple[float, int]:
    if lr <= 0 or tol <= 0 or max_steps < 0:
        raise ValueError("lr and tol must be positive, max_steps non-negative")
    x = float(x0)
    for step in range(max_steps):
        g = (f(x + h) - f(x - h)) / (2 * h)
        if abs(g) < tol:
            return x, step
        x -= lr * g
        if not math.isfinite(x) or abs(x) > 1e10:
            raise RuntimeError("diverged")
    return x, max_steps
