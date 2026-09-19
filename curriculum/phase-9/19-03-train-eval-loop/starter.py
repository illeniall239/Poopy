from typing import Callable

import torch
import torch.nn as nn

Batches = list[tuple[torch.Tensor, torch.Tensor]]


def train_and_eval(
    model: nn.Module,
    train: Batches,
    val: Batches,
    epochs: int,
    make_optimizer: Callable,
) -> dict[str, list[float]]:
    """Train each epoch, then compute the val loss in eval mode under no_grad; return per-epoch losses."""
    raise NotImplementedError
