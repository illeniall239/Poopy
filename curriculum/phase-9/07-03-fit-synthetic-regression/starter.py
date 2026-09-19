import torch
from torch import nn


def fit(X: torch.Tensor, y: torch.Tensor, epochs: int, lr: float) -> tuple[nn.Sequential, float]:
    """Train the given nn.Sequential with full-batch SGD on MSE; return the model in eval mode and its final MSE."""
    raise NotImplementedError
