import torch
from torch import nn


class BatchNorm1d(nn.Module):
    """BatchNorm over (N, num_features): batch statistics in training, running statistics in eval."""

    def __init__(self, num_features: int, eps: float = 1e-5, momentum: float = 0.1) -> None:
        """Create the parameters gamma (ones) and beta (zeros) and the buffers running_mean (zeros) and running_var (ones)."""
        super().__init__()
        raise NotImplementedError

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Normalize each column of x, using and updating the running stats according to self.training."""
        raise NotImplementedError
