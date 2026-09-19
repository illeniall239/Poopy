# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import torch
from torch import nn


def fit(X: torch.Tensor, y: torch.Tensor, epochs: int, lr: float) -> tuple[nn.Sequential, float]:
    if X.dim() != 2 or tuple(y.shape) != (X.shape[0], 1):
        raise ValueError("X must be (N, D) and y must be (N, 1)")
    if epochs < 0:
        raise ValueError("epochs must be >= 0")

    torch.manual_seed(0)
    model = nn.Sequential(nn.Linear(X.shape[1], 32), nn.ReLU(), nn.Dropout(0.1), nn.Linear(32, 1))
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()

    model.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(model(X), y)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        mse = loss_fn(model(X), y).item()
    return model, mse
