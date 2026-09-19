# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def _mse(xs: list[float], ys: list[float], w: float, b: float) -> float:
    return sum((w * x + b - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


def gd_linreg_1d(xs: list[float], ys: list[float], lr: float, epochs: int) -> tuple[float, float, list[float]]:
    if not xs or len(xs) != len(ys):
        raise ValueError("xs and ys must be non-empty and the same length")
    if lr <= 0:
        raise ValueError("lr must be positive")
    if epochs < 0:
        raise ValueError("epochs must be >= 0")
    n = len(xs)
    w, b = 0.0, 0.0
    history = [_mse(xs, ys, w, b)]
    for _ in range(epochs):
        errors = [w * x + b - y for x, y in zip(xs, ys)]
        grad_w = 2.0 / n * sum(e * x for e, x in zip(errors, xs))
        grad_b = 2.0 / n * sum(errors)
        w, b = w - lr * grad_w, b - lr * grad_b  # both from the same, old (w, b)
        history.append(_mse(xs, ys, w, b))
    return w, b, history
