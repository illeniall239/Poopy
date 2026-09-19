# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def fit_stump(xs: list[float], residuals: list[float]) -> tuple[float, float, float]:
    """The (threshold, left_value, right_value) that minimizes the squared error on the residuals."""
    values = sorted(set(xs))
    best, best_sse = None, float("inf")
    for lo, hi in zip(values, values[1:]):
        threshold = (lo + hi) / 2
        left = [r for x, r in zip(xs, residuals) if x <= threshold]
        right = [r for x, r in zip(xs, residuals) if x > threshold]
        left_value, right_value = mean(left), mean(right)
        sse = sum((r - left_value) ** 2 for r in left) + sum((r - right_value) ** 2 for r in right)
        if sse < best_sse - 1e-12:  # strict: ties keep the smaller threshold
            best, best_sse = (threshold, left_value, right_value), sse
    return best


def stump_predict(stump: tuple[float, float, float], x: float) -> float:
    threshold, left_value, right_value = stump
    return left_value if x <= threshold else right_value


def gradient_boost_stumps(xs: list[float], ys: list[float], n_rounds: int, lr: float) -> dict:
    if not xs or len(xs) != len(ys):
        raise ValueError("xs and ys must be non-empty and the same length")
    if len(set(xs)) < 2:
        raise ValueError("need at least two distinct x values to split")
    if n_rounds < 0 or not 0 < lr <= 1:
        raise ValueError("need n_rounds >= 0 and 0 < lr <= 1")
    base = mean(ys)
    predictions = [base] * len(ys)
    losses = [mean([(y - p) ** 2 for y, p in zip(ys, predictions)])]
    stumps = []
    for _ in range(n_rounds):
        residuals = [y - p for y, p in zip(ys, predictions)]  # the negative gradient of squared error / 2
        stump = fit_stump(xs, residuals)
        stumps.append(stump)
        predictions = [p + lr * stump_predict(stump, x) for x, p in zip(xs, predictions)]
        losses.append(mean([(y - p) ** 2 for y, p in zip(ys, predictions)]))
    return {"base": base, "lr": lr, "stumps": stumps, "losses": losses}


def predict_boosted(model: dict, x: float) -> float:
    return model["base"] + model["lr"] * sum(stump_predict(stump, x) for stump in model["stumps"])
