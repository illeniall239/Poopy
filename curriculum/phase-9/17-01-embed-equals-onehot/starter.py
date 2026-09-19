import torch


def embed(indices: torch.Tensor, table: torch.Tensor) -> torch.Tensor:
    """Return table rows for each index, shape indices.shape + (D,); ValueError if out of range."""
    raise NotImplementedError
