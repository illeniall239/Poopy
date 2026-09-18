# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import math


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def sigmoid_prime(x: float) -> float:
    s = sigmoid(x)
    return s * (1.0 - s)


def tanh(x: float) -> float:
    return math.tanh(x)


def tanh_prime(x: float) -> float:
    t = math.tanh(x)
    return 1.0 - t * t


def relu(x: float) -> float:
    return x if x > 0 else 0.0


def relu_prime(x: float) -> float:
    return 1.0 if x > 0 else 0.0
