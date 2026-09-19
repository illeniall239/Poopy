import torch
from torch import nn


class MLP(nn.Module):
    def __init__(self, sizes: list[int]):
        """Build one float64 nn.Linear per consecutive pair of sizes, stored in self.layers (nn.ModuleList)."""
        super().__init__()
        raise NotImplementedError

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Apply the layers in order with tanh after every layer except the last."""
        raise NotImplementedError


def load_weights(model: MLP, weights: list[tuple[list[list[float]], list[float]]]) -> None:
    """Copy (W, b) pairs, W shaped (out, in), into the model's existing parameters in place."""
    raise NotImplementedError


def loss_and_grads(model: MLP, X: torch.Tensor, y: torch.Tensor) -> tuple[float, list[torch.Tensor]]:
    """Mean squared error of model(X) against y, and a copy of every parameter's gradient."""
    raise NotImplementedError
