# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def fit_line(xs: list[float], ys: list[float]) -> tuple[float, float]:
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    if len(xs) < 2:
        raise ValueError("need at least 2 points")
    if all(x == xs[0] for x in xs):
        raise ValueError("all xs are equal; the slope is undefined")
    n = len(xs)
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    sxx = sum((x - x_mean) ** 2 for x in xs)
    sxy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    w = sxy / sxx
    b = y_mean - w * x_mean
    return w, b
