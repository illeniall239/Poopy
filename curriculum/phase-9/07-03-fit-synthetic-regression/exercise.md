# Fit a synthetic regression

Topic: 7. PyTorch fundamentals: tensors, autograd, nn.Module, the training loop
Difficulty: 2 of 3

## Problem

Write the standard PyTorch training loop from memory and score the trained model correctly.

`fit(X, y, epochs, lr)`:

- `X` is a float32 tensor of shape `(N, D)`; `y` is a float32 tensor of shape `(N, 1)`.
- First call `torch.manual_seed(0)`, so two calls with the same arguments give the same model.
- Build exactly this model:

  ```
  nn.Sequential(nn.Linear(D, 32), nn.ReLU(), nn.Dropout(0.1), nn.Linear(32, 1))
  ```

- Train it for `epochs` steps of full-batch gradient descent: each step runs on all of `X` at once, with `torch.optim.SGD(model.parameters(), lr=lr)` and mean squared error (`nn.MSELoss()`) as the loss. The model must be in training mode while it trains.
- After training, score the model on `X`, `y` in **evaluation mode** and without building a graph (`torch.no_grad()`).

Return `(model, mse)`: the trained model, left in evaluation mode, and that final mean squared error as a Python `float`. With `epochs == 0` there is no training step; you still return the scored untrained model.

Raise `ValueError` if `X` is not 2-D, if `y` does not have shape `(N, 1)`, or if `epochs` is negative.

On the test data (200 points, 2 features, `y = sin(2·x₀) + 0.5·x₁²`, variance about 0.69), `fit(X, y, 500, 0.1)` must reach an MSE below `0.02`.

## Examples

```
g = torch.Generator().manual_seed(0)
X = torch.rand(200, 2, generator=g) * 2 - 1
y = (torch.sin(2 * X[:, 0]) + 0.5 * X[:, 1] ** 2).unsqueeze(1)

model, mse = fit(X, y, 500, 0.1)
mse              → about 0.011        below 0.02
model.training   → False
fit(X, y, 0, 0.1)[1] → about 0.88     untrained
fit(X, y, -1, 0.1)   → ValueError
```

## Constraints

- `torch` on CPU; use `torch.optim.SGD` and `nn.MSELoss`.
- `N` at most 1000, `epochs` at most 2000.
- The returned `mse` must equal `nn.MSELoss()(model(X), y)` computed with the returned model under `torch.no_grad()`, within `1e-6`.

## Hints

1. What are the five things that happen in every training step, and in what order?
2. What does `.backward()` do to a `.grad` that already holds a value? Which call stops the last step's gradient from leaking into this one?
3. `nn.Dropout` behaves differently depending on one flag on the module. Which two methods set that flag, and which mode should the final score be computed in?
4. Scoring does not need gradients. What does `torch.no_grad()` save, and how do you turn a one-element loss tensor into a Python float?

## Explain-back

- Train it once with and once without `optimizer.zero_grad()`. What happens to the loss without it, and why does full-batch training make it so dramatic?
- The final score is lower in eval mode than in train mode on the same weights. Why? Which layer causes it here, and which other common layer would also misbehave without `model.eval()`?
- What does `torch.no_grad()` change about memory and speed, and does it change the numbers you get?
- Why does calling `torch.manual_seed(0)` make this function reproducible, and which two sources of randomness does it control here?
