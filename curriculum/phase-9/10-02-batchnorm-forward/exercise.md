# BatchNorm forward

Topic: 10. Normalization: BatchNorm and LayerNorm
Difficulty: 2 of 3

## Problem

Write `batchnorm_forward(batch, gamma, beta, running, momentum=0.1, training=True, eps=1e-5)` with plain tensor ops (no `nn.BatchNorm1d`, no `F.batch_norm`). `batch` has shape `(N, D)`: `N` examples, `D` features. `gamma` and `beta` have shape `(D,)`. `running` is a dict with two tensors of shape `(D,)`, `running["mean"]` and `running["var"]`, that persist between calls. Return the normalized batch, shape `(N, D)`.

BatchNorm normalizes each **feature column** over the **batch axis**:

- **Training mode** (`training=True`): use the batch's own statistics, per column: `mean = batch.mean(0)` and the **biased** variance `var` (divide by `N`). Output `gamma * (batch - mean) / sqrt(var + eps) + beta`. Then update the running statistics **in place** in the dict, with `momentum` weighting the new batch, exactly like `nn.BatchNorm1d`:
  - `running["mean"] ← (1 - momentum) * running["mean"] + momentum * mean`
  - `running["var"] ← (1 - momentum) * running["var"] + momentum * var_unbiased`, where `var_unbiased = var * N / (N - 1)` (PyTorch stores the **unbiased** estimate in the running variance even though it normalizes with the biased one).
  
  The running tensors are buffers, not parameters: the update must not be part of the autograd graph (after the call they must not require grad, even when `batch` does). `N = 1` makes the batch variance zero and `N / (N - 1)` undefined: raise `ValueError` and leave `running` untouched.
- **Eval mode** (`training=False`): normalize with `running["mean"]` and `running["var"]` instead of the batch's statistics, and do not modify `running` at all. Any `N >= 1` is fine here, including `N = 1`.

Tests compare against `nn.BatchNorm1d(D, eps=eps, momentum=momentum)` in both modes and check its `running_mean` / `running_var` after several training calls with the same momentum, all within `1e-5`.

## Examples

```
batch = tensor([[1., 10.], [3., 30.]]);  running = {"mean": zeros(2), "var": ones(2)}
batchnorm_forward(batch, ones(2), zeros(2), running, 0.1, True)
    → [[-1., -1.], [1., 1.]]       columns: mean (2, 20), biased var (1, 100)
    and afterwards running == {"mean": [0.2, 2.0], "var": [1.1, 20.9]}    unbiased var (2, 200)
batchnorm_forward(batch, ones(2), zeros(2), running, 0.1, False)
    → [[0.7628, 1.7499], [2.6697, 6.1247]]     (batch - 0.2) / sqrt(1.1 + eps), ...;  running unchanged
batchnorm_forward(tensor([[1., 10.]]), ones(2), zeros(2), running, 0.1, True)    → ValueError
batchnorm_forward(tensor([[1., 10.]]), ones(2), zeros(2), running, 0.1, False)   → [[0.7628, 1.7499]]
```

## Constraints

- `N` at most 1000, `D` at most 512.
- Values match `nn.BatchNorm1d` within `1e-5`.
- Tensor ops only; no Python loops over rows or columns.

## Hints

1. LayerNorm reduced over `dim=-1`. Which `dim` does BatchNorm reduce over, and what shape do `mean` and `var` have afterwards? Does the subtraction still broadcast against `(N, D)`?
2. PyTorch's `torch.var` defaults to `unbiased=True`. Which estimate does the normalization need, which does the running variance need, and what single factor converts one into the other?
3. What is the batch variance when `N = 1`, and what does that do to `(batch - mean) / sqrt(var + eps)`? Where in the function should you check `N` so that `running` is never half-updated?
4. If `batch` requires grad, then `mean` and `var` do too. What tool (`torch.no_grad()` or `.detach()`) keeps that history out of the running buffers, and why would a training loop eventually break without it?

## Explain-back

- Why does inference use the running statistics rather than the batch's own? What would happen to a single example's prediction if you forgot and left training mode on?
- In training mode the output for one example depends on the other examples in its batch. Why is that "noise" sometimes described as a regularizer, and why does it become a problem for tiny batches?
- Why is the bias of the linear layer feeding a BatchNorm redundant? Walk through what subtracting the column mean does to it.
- What are `gamma` and `beta` for, and how are they updated during training? What would you lose if they were fixed at 1 and 0?
