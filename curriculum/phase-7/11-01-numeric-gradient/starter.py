from collections.abc import Callable


def numeric_gradient(f: Callable[[list[float]], float], params: list[float], h: float = 1e-5) -> list[float]:
    """Central-difference partial derivative of f for every entry of params; ValueError if h <= 0."""
    raise NotImplementedError
