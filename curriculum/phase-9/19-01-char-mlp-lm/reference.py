# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import torch
import torch.nn as nn
import torch.nn.functional as F

CHARS = ".abcdefghijklmnopqrstuvwxyz"
INDEX = {ch: i for i, ch in enumerate(CHARS)}


class CharMLP(nn.Module):
    def __init__(self, vocab: int, block: int, dim: int, hidden: int):
        super().__init__()
        self.emb = nn.Embedding(vocab, dim)
        self.hidden = nn.Linear(block * dim, hidden)
        self.out = nn.Linear(hidden, vocab)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        e = self.emb(x).flatten(start_dim=1)  # (B, block * dim): the embeddings of the context, side by side
        return self.out(torch.tanh(self.hidden(e)))


def make_dataset(words: list[str], block: int) -> tuple[torch.Tensor, torch.Tensor]:
    X, Y = [], []
    for word in words:
        if any(ch not in INDEX or ch == "." for ch in word):
            raise ValueError(f"{word!r} must contain only a-z")
        context = [0] * block
        for ch in word + ".":
            ix = INDEX[ch]
            X.append(context)
            Y.append(ix)
            context = context[1:] + [ix]
    return torch.tensor(X, dtype=torch.long).reshape(-1, block), torch.tensor(Y, dtype=torch.long)


def train_lm(model: nn.Module, X: torch.Tensor, Y: torch.Tensor, steps: int, lr: float) -> list[float]:
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    losses = []
    for _ in range(steps):
        loss = F.cross_entropy(model(X), Y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    return losses
