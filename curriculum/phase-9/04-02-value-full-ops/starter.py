from __future__ import annotations


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
        """Return self ** k for a plain number k; raise TypeError otherwise."""
        raise NotImplementedError

    def tanh(self) -> Value:
        """Return tanh(self)."""
        raise NotImplementedError

    def exp(self) -> Value:
        """Return e ** self."""
        raise NotImplementedError

    def relu(self) -> Value:
        """Return max(0, self); derivative 0 at exactly 0."""
        raise NotImplementedError

    def __neg__(self) -> Value:
        """Return -self, built from existing ops."""
        raise NotImplementedError

    def __sub__(self, other: Value | float) -> Value:
        """Return self - other, built from existing ops."""
        raise NotImplementedError

    def __truediv__(self, other: Value | float) -> Value:
        """Return self / other, built from existing ops."""
        raise NotImplementedError

    def __radd__(self, other: float) -> Value:
        """Return other + self for a plain number on the left."""
        raise NotImplementedError

    def __rmul__(self, other: float) -> Value:
        """Return other * self for a plain number on the left."""
        raise NotImplementedError

    def __rsub__(self, other: float) -> Value:
        """Return other - self for a plain number on the left."""
        raise NotImplementedError

    def __rtruediv__(self, other: float) -> Value:
        """Return other / self for a plain number on the left."""
        raise NotImplementedError

    def backward(self) -> None:
        """Set self.grad = 1 and fill .grad of every value self depends on, in reverse topological order."""
        raise NotImplementedError
