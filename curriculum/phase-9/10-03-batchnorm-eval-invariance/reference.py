# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import torch
from torch import nn


class BatchNorm1d(nn.Module):
    def __init__(self, num_features: int, eps: float = 1e-5, momentum: float = 0.1) -> None:
        super().__init__()
        self.num_features = num_features
        self.eps = eps
        self.momentum = momentum
        self.gamma = nn.Parameter(torch.ones(num_features))
        self.beta = nn.Parameter(torch.zeros(num_features))
        self.register_buffer("running_mean", torch.zeros(num_features))
        self.register_buffer("running_var", torch.ones(num_features))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() != 2 or x.shape[1] != self.num_features:
            raise ValueError(f"expected shape (N, {self.num_features}), got {tuple(x.shape)}")
        n = x.shape[0]
        if self.training:
            if n < 2:
                raise ValueError("BatchNorm needs at least 2 examples in training mode")
            mean = x.mean(dim=0)
            var = x.var(dim=0, unbiased=False)
            with torch.no_grad():
                self.running_mean.mul_(1 - self.momentum).add_(self.momentum * mean)
                self.running_var.mul_(1 - self.momentum).add_(self.momentum * var * n / (n - 1))
        else:
            mean = self.running_mean
            var = self.running_var
        x_hat = (x - mean) / torch.sqrt(var + self.eps)
        return self.gamma * x_hat + self.beta
