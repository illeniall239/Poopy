from __future__ import annotations


class Value:
    """A scalar that records the operations that produced it, for reverse-mode autodiff."""

    def __init__(self, data: float, _children: tuple[Value, ...] = (), _op: str = ""):
        """Store data, start grad at 0.0, remember the children and op."""
        raise NotImplementedError

    def __add__(self, other: Value | float) -> Value:
        """Return self + other; plain numbers are wrapped in a Value."""
        raise NotImplementedError

    def __mul__(self, other: Value | float) -> Value:
        """Return self * other; plain numbers are wrapped in a Value."""
        raise NotImplementedError

    def tanh(self) -> Value:
        """Return tanh(self)."""
        raise NotImplementedError

    def backward(self) -> None:
        """Set self.grad = 1 and fill .grad of every value self depends on, in reverse topological order."""
        raise NotImplementedError
