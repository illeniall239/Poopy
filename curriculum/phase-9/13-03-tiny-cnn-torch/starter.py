import torch
from torch import nn


class TinyCNN(nn.Module):
    """conv1 -> ReLU -> pool1 -> conv2 -> ReLU -> pool2 -> flatten -> fc, for 1x8x8 inputs and 2 classes."""

    def __init__(self) -> None:
        """Create conv1, pool1, conv2, pool2 and fc."""
        super().__init__()
        raise NotImplementedError

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Return logits of shape (B, 2)."""
        raise NotImplementedError


def train_tiny_cnn(model: nn.Module, X: torch.Tensor, y: torch.Tensor, steps: int, lr: float) -> list[float]:
    """Full-batch Adam + cross-entropy for `steps` steps; return the loss at each step."""
    raise NotImplementedError
