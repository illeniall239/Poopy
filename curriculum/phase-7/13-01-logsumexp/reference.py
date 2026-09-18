# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import math


def logsumexp(xs: list[float]) -> float:
    if not xs:
        raise ValueError("empty input")
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))


def log_softmax(xs: list[float]) -> list[float]:
    lse = logsumexp(xs)
    return [x - lse for x in xs]


def softmax(xs: list[float]) -> list[float]:
    return [math.exp(v) for v in log_softmax(xs)]
