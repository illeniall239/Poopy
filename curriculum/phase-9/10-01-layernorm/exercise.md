# LayerNorm

Topic: 10. Normalization: BatchNorm and LayerNorm
Difficulty: 1 of 3

## Problem

Write `layernorm(x, gamma, beta, eps=1e-5)` with plain tensor ops (no `nn.LayerNorm`, no `F.layer_norm`). `x` is a tensor whose **last** dimension is the feature dimension `D`, usually shape `(B, D)`. For every row (every index over the leading dimensions) it:

1. subtracts that row's mean over its `D` features,
2. divides by `sqrt(var + eps)`, where `var` is the **biased** variance over the same `D` features (divide by `D`, not `D - 1`), like PyTorch,
3. multiplies by `gamma` and adds `beta`, both tensors of shape `(D,)`.

Return a new tensor of the same shape as `x`. Each row is normalized on its own: the rows of `x` never see each other, so the output for a row does not depend on which other rows are in the batch, and a batch of one row works. Before `gamma` and `beta` are applied every row has mean ≈ 0 and variance ≈ 1; a row of identical values gives exactly `beta` (the `eps` keeps the division finite). `gamma` and `beta` are learned: when they require grad, the result must be differentiable with respect to them.

Raise `ValueError` if `gamma` or `beta` does not have shape `(D,)`. Tests compare against `torch.nn.functional.layer_norm` within `1e-5`.

## Examples

```
layernorm(tensor([[1., 2., 3.]]), ones(3), zeros(3))          → [[-1.2247, 0.0000, 1.2247]]
layernorm(tensor([[1., 2., 3.]]), tensor([2., 2., 2.]), tensor([1., 1., 1.]))
                                                              → [[-1.4495, 1.0000, 3.4495]]
layernorm(tensor([[5., 5., 5., 5.]]), ones(4), zeros(4))      → [[0., 0., 0., 0.]]
layernorm(tensor([[1., 2.], [10., 20.]]), ones(2), zeros(2))  → [[-1., 1.], [-1., 1.]]    each row on its own
layernorm(x_of_shape_(4, 6), ones(3), zeros(3))               → ValueError
```

## Constraints

- `x` has at most 1000 rows and `D` is at most 512; `x` may have extra leading dimensions, e.g. `(B, T, D)`.
- Match `F.layer_norm(x, (D,), gamma, beta, eps)` within `1e-5`.
- Use tensor ops only; no loops over rows.

## Hints

1. Which axis holds the features of one example? When you call `mean` and `var`, which `dim` argument picks that axis, and what does `keepdim=True` do for the subtraction that follows?
2. `torch.var` divides by `n - 1` by default. Which keyword switches it to the biased estimate the exercise (and PyTorch) uses?
3. Where exactly does `eps` go: inside the square root, outside it, or added to the standard deviation? Which choice keeps a constant row from producing NaN?
4. `gamma` has shape `(D,)` and the normalized tensor has shape `(B, D)`. How does broadcasting line them up, and why does that make the same scale apply to every row?

## Explain-back

- LayerNorm computes statistics over which axis? If you put a new row into the batch, which outputs change?
- BatchNorm has a train mode and an eval mode. Why does LayerNorm need neither?
- If `gamma` and `beta` were fixed at 1 and 0, what could the layer after LayerNorm no longer express? Why are they parameters?
- Why does a transformer normalize with LayerNorm rather than BatchNorm? (Think about variable-length sequences and batches of size 1 at generation time.)
