# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math

SQRT_2_OVER_PI = math.sqrt(2.0 / math.pi)


def gelu_exact(x: float) -> float:
    return 0.5 * x * (1.0 + math.erf(x / math.sqrt(2.0)))


def gelu_tanh(x: float) -> float:
    return 0.5 * x * (1.0 + math.tanh(SQRT_2_OVER_PI * (x + 0.044715 * x ** 3)))
