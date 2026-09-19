# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import torch


def batchnorm_forward(
    batch: torch.Tensor,
    gamma: torch.Tensor,
    beta: torch.Tensor,
    running: dict[str, torch.Tensor],
    momentum: float = 0.1,
    training: bool = True,
    eps: float = 1e-5,
) -> torch.Tensor:
    n = batch.shape[0]
    if training:
        if n < 2:
            raise ValueError("BatchNorm needs at least 2 examples in training mode")
        mean = batch.mean(dim=0)
        var = batch.var(dim=0, unbiased=False)
        with torch.no_grad():
            running["mean"] = (1 - momentum) * running["mean"] + momentum * mean
            running["var"] = (1 - momentum) * running["var"] + momentum * var * n / (n - 1)
    else:
        mean = running["mean"]
        var = running["var"]
    x_hat = (batch - mean) / torch.sqrt(var + eps)
    return gamma * x_hat + beta
