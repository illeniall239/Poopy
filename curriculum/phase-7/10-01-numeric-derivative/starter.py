from collections.abc import Callable


def numeric_derivative(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Central difference (f(x+h) - f(x-h)) / (2h); ValueError if h <= 0."""
    raise NotImplementedError


def forward_derivative(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Forward difference (f(x+h) - f(x)) / h; ValueError if h <= 0."""
    raise NotImplementedError
