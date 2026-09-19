# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import torch
from torch import nn


class MLP(nn.Module):
    def __init__(self, sizes: list[int]):
        super().__init__()
        if len(sizes) < 2:
            raise ValueError("need at least an input and an output size")
        self.layers = nn.ModuleList(
            nn.Linear(n_in, n_out, dtype=torch.float64) for n_in, n_out in zip(sizes, sizes[1:])
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for i, layer in enumerate(self.layers):
            x = layer(x)
            if i < len(self.layers) - 1:
                x = torch.tanh(x)
        return x


def load_weights(model: MLP, weights: list[tuple[list[list[float]], list[float]]]) -> None:
    if len(weights) != len(model.layers):
        raise ValueError(f"expected {len(model.layers)} (W, b) pairs, got {len(weights)}")
    with torch.no_grad():
        for layer, (W, b) in zip(model.layers, weights):
            W = torch.tensor(W, dtype=torch.float64)
            b = torch.tensor(b, dtype=torch.float64)
            if W.shape != layer.weight.shape or b.shape != layer.bias.shape:
                raise ValueError(f"expected W {tuple(layer.weight.shape)} and b {tuple(layer.bias.shape)}")
            layer.weight.copy_(W)
            layer.bias.copy_(b)


def loss_and_grads(model: MLP, X: torch.Tensor, y: torch.Tensor) -> tuple[float, list[torch.Tensor]]:
    model.zero_grad()
    loss = ((model(X) - y) ** 2).mean()
    loss.backward()
    return loss.item(), [p.grad.clone() for p in model.parameters()]
