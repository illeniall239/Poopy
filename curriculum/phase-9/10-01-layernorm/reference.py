# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import torch


def layernorm(x: torch.Tensor, gamma: torch.Tensor, beta: torch.Tensor, eps: float = 1e-5) -> torch.Tensor:
    d = x.shape[-1]
    if gamma.shape != (d,) or beta.shape != (d,):
        raise ValueError(f"gamma and beta must have shape ({d},)")
    mean = x.mean(dim=-1, keepdim=True)
    var = x.var(dim=-1, unbiased=False, keepdim=True)
    x_hat = (x - mean) / torch.sqrt(var + eps)
    return x_hat * gamma + beta
