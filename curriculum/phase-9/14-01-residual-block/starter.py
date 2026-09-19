from typing import Callable

import torch
from torch import nn


def residual_block_forward(x: list[float], f: Callable[[list[float]], list[float]]) -> list[float]:
    """Return x + f(x) elementwise; ValueError if f(x) has a different length."""
    raise NotImplementedError


class ResidualMLP(nn.Module):
    """x + f(x) with f = Linear(dim, hidden) -> ReLU -> Linear(hidden, dim)."""

    def __init__(self, dim: int, hidden: int) -> None:
        """Create self.f."""
        super().__init__()
        raise NotImplementedError

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Return x + self.f(x)."""
        raise NotImplementedError
