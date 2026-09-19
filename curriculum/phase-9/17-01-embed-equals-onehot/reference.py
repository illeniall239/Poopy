# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import torch


def embed(indices: torch.Tensor, table: torch.Tensor) -> torch.Tensor:
    if indices.numel() and (indices.min() < 0 or indices.max() >= table.shape[0]):
        raise ValueError("index out of range for the embedding table")
    return table[indices]
