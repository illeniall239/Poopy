from collections.abc import Callable

Pair = tuple[Callable[[float], float], Callable[[float], float]]


def compose(chain: list[Pair], x: float) -> float:
    """Apply the functions of chain in order to x."""
    raise NotImplementedError


def intermediates(chain: list[Pair], x: float) -> list[float]:
    """[x, f1(x), f2(f1(x)), ..., y]."""
    raise NotImplementedError


def chain_derivative(chain: list[Pair], x: float) -> float:
    """dy/dx by the chain rule, each derivative evaluated at its own input; 1.0 for an empty chain."""
    raise NotImplementedError
