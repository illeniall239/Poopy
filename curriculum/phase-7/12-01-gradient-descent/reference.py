# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
from collections.abc import Callable


def gradient_descent(
    grad_f: Callable[[list[float]], list[float]], x0: list[float], lr: float, steps: int
) -> list[list[float]]:
    if lr <= 0 or steps < 0:
        raise ValueError("lr must be positive and steps non-negative")
    x = list(x0)
    trajectory = [x]
    for _ in range(steps):
        g = grad_f(x)
        x = [xi - lr * gi for xi, gi in zip(x, g)]
        trajectory.append(x)
    return trajectory
