# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from collections.abc import Callable


def numeric_derivative(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    if h <= 0:
        raise ValueError("h must be positive")
    return (f(x + h) - f(x - h)) / (2 * h)


def forward_derivative(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    if h <= 0:
        raise ValueError("h must be positive")
    return (f(x + h) - f(x)) / h
