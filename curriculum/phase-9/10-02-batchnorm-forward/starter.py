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
    """BatchNorm over the batch axis of (N, D): batch stats and an in-place running-stat update in training, running stats in eval."""
    raise NotImplementedError
