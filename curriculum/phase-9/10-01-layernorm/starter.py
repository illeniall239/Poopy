import torch


def layernorm(x: torch.Tensor, gamma: torch.Tensor, beta: torch.Tensor, eps: float = 1e-5) -> torch.Tensor:
    """Normalize each row of x over its last (feature) dimension, then scale by gamma and shift by beta."""
    raise NotImplementedError
