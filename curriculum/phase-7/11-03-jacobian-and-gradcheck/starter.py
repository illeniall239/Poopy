from collections.abc import Callable


def numeric_jacobian(f: Callable[[list[float]], list[float]], x: list[float], h: float = 1e-5) -> list[list[float]]:
    """m×n matrix J[i][j] = df_i/dx_j by central differences; ValueError if h <= 0 or x is empty."""
    raise NotImplementedError


def gradient_check(analytic: list[float], numeric: list[float]) -> float:
    """Relative error ||a - n|| / max(||a|| + ||n||, 1e-12); ValueError on length mismatch."""
    raise NotImplementedError
