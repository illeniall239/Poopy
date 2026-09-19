# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def _residuals(y: list[float], yhat: list[float], delta: float) -> list[float]:
    if not y or len(y) != len(yhat):
        raise ValueError("y and yhat must be non-empty and the same length")
    if delta <= 0:
        raise ValueError("delta must be positive")
    return [p - t for t, p in zip(y, yhat)]


def huber(y: list[float], yhat: list[float], delta: float = 1.0) -> float:
    rs = _residuals(y, yhat, delta)
    total = 0.0
    for r in rs:
        if abs(r) <= delta:
            total += 0.5 * r * r                    # quadratic, like MSE
        else:
            total += delta * (abs(r) - 0.5 * delta)  # linear, like L1
    return total / len(rs)


def huber_grad(y: list[float], yhat: list[float], delta: float = 1.0) -> list[float]:
    rs = _residuals(y, yhat, delta)
    n = len(rs)
    # inside the band the slope is r; outside it is capped at +/- delta
    return [(r if abs(r) <= delta else math.copysign(delta, r)) / n for r in rs]
