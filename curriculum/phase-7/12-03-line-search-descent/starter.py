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
    """Largest alpha in alpha0 * beta^k satisfying Armijo f(x - alpha g) <= fx - c alpha |g|^2."""
    raise NotImplementedError


def line_search_descent(
    f: Callable[[list[float]], float],
    grad_f: Callable[[list[float]], list[float]],
    x0: list[float],
    tol: float = 1e-6,
    max_steps: int = 1000,
) -> tuple[list[float], int]:
    """Gradient descent with backtracking line search; stops when |grad| < tol or after max_steps."""
    raise NotImplementedError
