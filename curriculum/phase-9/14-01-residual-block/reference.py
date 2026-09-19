# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Callable

import torch
from torch import nn


def residual_block_forward(x: list[float], f: Callable[[list[float]], list[float]]) -> list[float]:
    fx = f(x)
    if len(fx) != len(x):
        raise ValueError("f(x) must have the same length as x")
    return [a + b for a, b in zip(x, fx)]


class ResidualMLP(nn.Module):
    def __init__(self, dim: int, hidden: int) -> None:
        super().__init__()
        self.f = nn.Sequential(nn.Linear(dim, hidden), nn.ReLU(), nn.Linear(hidden, dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.f(x)
