from __future__ import annotations

import random


class Value:
    """A scalar that records the operations that produced it, for reverse-mode autodiff."""

    def __init__(self, data: float, _children: tuple[Value, ...] = (), _op: str = ""):
        """Store data, start grad at 0.0, remember the children and op."""
        raise NotImplementedError

    def __add__(self, other: Value | float) -> Value:
        """Return self + other."""
        raise NotImplementedError

    def __mul__(self, other: Value | float) -> Value:
        """Return self * other."""
        raise NotImplementedError

    def __pow__(self, k: int | float) -> Value:
        """Return self ** k for a plain number k."""
        raise NotImplementedError

    def tanh(self) -> Value:
        """Return tanh(self)."""
        raise NotImplementedError

    def __neg__(self) -> Value:
        """Return -self."""
        raise NotImplementedError

    def __sub__(self, other: Value | float) -> Value:
        """Return self - other."""
        raise NotImplementedError

    def __radd__(self, other: float) -> Value:
        """Return other + self."""
        raise NotImplementedError

    def __rmul__(self, other: float) -> Value:
        """Return other * self."""
        raise NotImplementedError

    def __rsub__(self, other: float) -> Value:
        """Return other - self."""
        raise NotImplementedError

    def backward(self) -> None:
        """Set self.grad = 1 and fill .grad of every value self depends on, in reverse topological order."""
        raise NotImplementedError


class Neuron:
    def __init__(self, nin: int, rng: random.Random):
        """Create nin weights then a bias, each Value(rng.uniform(-1, 1))."""
        raise NotImplementedError

    def __call__(self, x: list[Value | float]) -> Value:
        """Return tanh(w . x + b)."""
        raise NotImplementedError

    def parameters(self) -> list[Value]:
        """Return the weights followed by the bias."""
        raise NotImplementedError


class Layer:
    def __init__(self, nin: int, nout: int, rng: random.Random):
        """Create nout neurons in order from rng."""
        raise NotImplementedError

    def __call__(self, x: list[Value | float]) -> list[Value]:
        """Return the list of neuron outputs."""
        raise NotImplementedError

    def parameters(self) -> list[Value]:
        """Return every neuron's parameters, in order."""
        raise NotImplementedError


class MLP:
    def __init__(self, nin: int, nouts: list[int], seed: int = 0):
        """Create layers [nin] + nouts, all drawn from one random.Random(seed)."""
        raise NotImplementedError

    def __call__(self, x: list[Value | float]) -> Value | list[Value]:
        """Run x through every layer; return a single Value if the last layer has one unit."""
        raise NotImplementedError

    def parameters(self) -> list[Value]:
        """Return every layer's parameters, in order."""
        raise NotImplementedError

    def zero_grad(self) -> None:
        """Set every parameter's grad to 0.0."""
        raise NotImplementedError


def train(model: MLP, xs: list[list[float]], ys: list[float], steps: int, lr: float) -> list[float]:
    """Gradient descent on the summed squared error; return the loss before each step's update."""
    raise NotImplementedError
