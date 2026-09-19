# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from __future__ import annotations

import math


class Value:
    def __init__(self, data: float, _children: tuple[Value, ...] = (), _op: str = ""):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    # --- primitive ops: each one knows its own local derivative ---

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

    def exp(self) -> Value:
        out = Value(math.exp(self.data), (self,), "exp")

        def _backward():
            self.grad += out.data * out.grad

        out._backward = _backward
        return out

    def relu(self) -> Value:
        out = Value(self.data if self.data > 0 else 0.0, (self,), "relu")

        def _backward():
            self.grad += (1.0 if self.data > 0 else 0.0) * out.grad

        out._backward = _backward
        return out

    # --- composed ops: no new calculus, the primitives do the work ---

    def __neg__(self) -> Value:
        return self * -1

    def __sub__(self, other: Value | float) -> Value:
        return self + (-other)

    def __truediv__(self, other: Value | float) -> Value:
        other = other if isinstance(other, Value) else Value(other)
        return self * other ** -1

    def __radd__(self, other: float) -> Value:  # other + self
        return self + other

    def __rmul__(self, other: float) -> Value:  # other * self
        return self * other

    def __rsub__(self, other: float) -> Value:  # other - self
        return other + (-self)

    def __rtruediv__(self, other: float) -> Value:  # other / self
        return other * self ** -1

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

    def __repr__(self) -> str:
        return f"Value(data={self.data}, grad={self.grad})"
