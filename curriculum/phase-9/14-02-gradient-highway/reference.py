# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math

import torch


def chain_grad(derivs: list[float], residual: bool) -> float:
    return float(math.prod(1 + d if residual else d for d in derivs))


def input_grad_norm(depth: int, width: int, residual: bool, seed: int) -> float:
    if depth < 0 or width < 1:
        raise ValueError("need depth >= 0 and width >= 1")
    torch.manual_seed(seed)
    weights = [torch.randn(width, width) * 0.5 / math.sqrt(width) for _ in range(depth)]
    x = torch.randn(1, width, requires_grad=True)
    h = x
    for W in weights:
        z = torch.tanh(h @ W.T)
        h = h + z if residual else z
    h.sum().backward()
    return x.grad.norm().item()
