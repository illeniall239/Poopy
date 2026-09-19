def solve(a: list[list[float]], b: list[float]) -> list[float]:
    """x with a @ x == b by Gaussian elimination with partial pivoting; ValueError if singular or mismatched."""
    raise NotImplementedError


def polynomial_features(xs: list[float], degree: int) -> list[list[float]]:
    """Rows [1, x, x**2, ..., x**degree]; ValueError if degree < 0."""
    raise NotImplementedError


def fit_polynomial(xs: list[float], ys: list[float], degree: int) -> list[float]:
    """Least-squares coefficients [c0, ..., c_degree] from the normal equations solved with solve()."""
    raise NotImplementedError
