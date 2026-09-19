# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Callable

import torch
import torch.nn as nn
import torch.nn.functional as F

Batches = list[tuple[torch.Tensor, torch.Tensor]]


def train_and_eval(
    model: nn.Module,
    train: Batches,
    val: Batches,
    epochs: int,
    make_optimizer: Callable,
) -> dict[str, list[float]]:
    if epochs < 1 or not train or not val:
        raise ValueError("need at least one epoch, one train batch and one val batch")
    optimizer = make_optimizer(model.parameters())
    history = {"train": [], "val": []}
    for _ in range(epochs):
        model.train()
        total, count = 0.0, 0
        for X, y in train:
            loss = F.cross_entropy(model(X), y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total += loss.item() * len(y)
            count += len(y)
        history["train"].append(total / count)

        model.eval()
        total, count = 0.0, 0
        with torch.no_grad():
            for X, y in val:
                total += F.cross_entropy(model(X), y, reduction="sum").item()
                count += len(y)
        history["val"].append(total / count)
    return history
