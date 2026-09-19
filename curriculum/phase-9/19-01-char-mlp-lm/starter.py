import torch
import torch.nn as nn


class CharMLP(nn.Module):
    def __init__(self, vocab: int, block: int, dim: int, hidden: int):
        """Create a shared (vocab, dim) embedding, Linear(block*dim, hidden) + tanh, Linear(hidden, vocab)."""
        super().__init__()
        raise NotImplementedError

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Map a (B, block) long tensor of contexts to (B, vocab) logits."""
        raise NotImplementedError


def make_dataset(words: list[str], block: int) -> tuple[torch.Tensor, torch.Tensor]:
    """Return (X, Y): every (context of block indices, next index) pair, "." = 0 padding and end marker."""
    raise NotImplementedError


def train_lm(model: nn.Module, X: torch.Tensor, Y: torch.Tensor, steps: int, lr: float) -> list[float]:
    """Full-batch Adam on cross-entropy for steps steps; return each step's loss before its update."""
    raise NotImplementedError
