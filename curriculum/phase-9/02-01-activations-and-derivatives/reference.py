# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)  # x < 0, so this cannot overflow
    return e / (1.0 + e)


def d_sigmoid(x: float) -> float:
    s = sigmoid(x)
    return s * (1.0 - s)


def tanh(x: float) -> float:
    return math.tanh(x)


def d_tanh(x: float) -> float:
    return 1.0 - math.tanh(x) ** 2


def relu(x: float) -> float:
    return x if x > 0 else 0.0


def d_relu(x: float) -> float:
    return 1.0 if x > 0 else 0.0


def leaky_relu(x: float, alpha: float = 0.01) -> float:
    return x if x > 0 else alpha * x


def d_leaky_relu(x: float, alpha: float = 0.01) -> float:
    return 1.0 if x > 0 else alpha


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _normal_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def gelu(x: float) -> float:
    return x * _normal_cdf(x)


def d_gelu(x: float) -> float:
    # product rule: d/dx [x * Phi(x)] = Phi(x) + x * phi(x)
    return _normal_cdf(x) + x * _normal_pdf(x)
