# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from __future__ import annotations

import math
import random


class Value:
    def __init__(self, data: float, _children: tuple[Value, ...] = (), _op: str = ""):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def __add__(self, other: Value | float) -> Value:
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            self.grad += out.grad
            other.grad += out.grad

        out._backward = _backward
        return out

    def __mul__(self, other: Value | float) -> Value:
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward
        return out

    def __pow__(self, k: int | float) -> Value:
        if isinstance(k, bool) or not isinstance(k, (int, float)):
            raise TypeError("only int/float exponents are supported")
        out = Value(self.data ** k, (self,), f"**{k}")

        def _backward():
            self.grad += k * self.data ** (k - 1) * out.grad

        out._backward = _backward
        return out

    def tanh(self) -> Value:
        t = math.tanh(self.data)
        out = Value(t, (self,), "tanh")

        def _backward():
            self.grad += (1 - t ** 2) * out.grad

        out._backward = _backward
        return out

    def __neg__(self) -> Value:
        return self * -1

    def __sub__(self, other: Value | float) -> Value:
        return self + (-other)

    def __radd__(self, other: float) -> Value:
        return self + other

    def __rmul__(self, other: float) -> Value:
        return self * other

    def __rsub__(self, other: float) -> Value:
        return other + (-self)

    def backward(self) -> None:
        topo, visited = [], set()

        def build(v: Value) -> None:
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build(child)
                topo.append(v)

        build(self)
        self.grad = 1.0
        for v in reversed(topo):
            v._backward()


class Neuron:
    def __init__(self, nin: int, rng: random.Random):
        self.w = [Value(rng.uniform(-1, 1)) for _ in range(nin)]
        self.b = Value(rng.uniform(-1, 1))

    def __call__(self, x: list[Value | float]) -> Value:
        act = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
        return act.tanh()

    def parameters(self) -> list[Value]:
        return self.w + [self.b]


class Layer:
    def __init__(self, nin: int, nout: int, rng: random.Random):
        self.neurons = [Neuron(nin, rng) for _ in range(nout)]

    def __call__(self, x: list[Value | float]) -> list[Value]:
        return [n(x) for n in self.neurons]

    def parameters(self) -> list[Value]:
        return [p for n in self.neurons for p in n.parameters()]


class MLP:
    def __init__(self, nin: int, nouts: list[int], seed: int = 0):
        rng = random.Random(seed)
        sizes = [nin] + nouts
        self.layers = [Layer(sizes[i], sizes[i + 1], rng) for i in range(len(nouts))]

    def __call__(self, x: list[Value | float]) -> Value | list[Value]:
        for layer in self.layers:
            x = layer(x)
        return x[0] if len(x) == 1 else x

    def parameters(self) -> list[Value]:
        return [p for layer in self.layers for p in layer.parameters()]

    def zero_grad(self) -> None:
        for p in self.parameters():
            p.grad = 0.0


def train(model: MLP, xs: list[list[float]], ys: list[float], steps: int, lr: float) -> list[float]:
    losses = []
    for _ in range(steps):
        ypred = [model(x) for x in xs]
        loss = sum(((yp - yt) ** 2 for yp, yt in zip(ypred, ys)), Value(0.0))
        losses.append(loss.data)

        model.zero_grad()  # otherwise this step's gradients pile onto the last step's
        loss.backward()
        for p in model.parameters():
            p.data -= lr * p.grad
    return losses
