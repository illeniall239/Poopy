# BatchNorm eval invariance

Topic: 10. Normalization: BatchNorm and LayerNorm
Difficulty: 2 of 3

## Problem

Write a `BatchNorm1d(num_features, eps=1e-5, momentum=0.1)` class, an `nn.Module`, from tensor ops (no `nn.BatchNorm1d`, no `F.batch_norm`). It behaves like PyTorch's layer of the same name on inputs of shape `(N, num_features)`, and the point of the exercise is the property in the title: **in eval mode the output for one example is identical whatever batch it is placed in**, while in training mode it is not.

- `__init__` creates two learned parameters, `self.gamma = nn.Parameter(torch.ones(num_features))` and `self.beta = nn.Parameter(torch.zeros(num_features))`, and two buffers registered with `self.register_buffer`, `running_mean` (zeros) and `running_var` (ones), both of shape `(num_features,)`. `parameters()` must yield exactly `gamma` and `beta`; the buffers appear in `state_dict()` but never in `parameters()`.
- `forward(x)` reads `self.training` (toggled by the inherited `.train()` / `.eval()`):
  - **training**: per column, `mean = x.mean(0)` and the **biased** variance `var` (divide by `N`); output `gamma * (x - mean) / sqrt(var + eps) + beta`. Then, outside the autograd graph, update the buffers in place with `momentum` weighting the new batch: `running_mean ← (1 - momentum) * running_mean + momentum * mean` and `running_var ← (1 - momentum) * running_var + momentum * var * N / (N - 1)` (the **unbiased** batch variance, as PyTorch stores it). If `N = 1`, raise `ValueError` before touching the buffers.
  - **eval**: output `gamma * (x - running_mean) / sqrt(running_var + eps) + beta`; the buffers are not modified; any `N >= 1` works.
- Raise `ValueError` if `x` is not 2-D with `num_features` columns.

Tests build `nn.BatchNorm1d(num_features, eps=eps, momentum=momentum)` with the same `gamma`/`beta` and feed it the same batches, and compare outputs and running statistics within `1e-5`. They also check that a row gives the same eval output whether it sits in batch A or batch B (`1e-6`), that its train-mode outputs in those two batches differ, and that a single-example batch raises `ValueError` in training mode but works in eval mode.

## Examples

```
bn = BatchNorm1d(2)
bn.train()
bn(tensor([[1., 10.], [3., 30.]]))         → [[-1., -1.], [1., 1.]]
bn.running_mean, bn.running_var            → [0.2, 2.0], [1.1, 20.9]
bn(tensor([[1., 10.]]))                    → ValueError            (batch of one in training mode)
bn.eval()
bn(tensor([[1., 10.]]))                    → [[0.7628, 1.7499]]
bn(tensor([[1., 10.], [100., -5.]]))[0]    → [0.7628, 1.7499]      same row, same answer, any batch
bn.running_mean                            → [0.2, 2.0]            untouched by eval calls
[p.shape for p in bn.parameters()]         → [(2,), (2,)]
```

## Constraints

- `num_features` at most 512, batches at most 1000 rows.
- Values match `nn.BatchNorm1d` within `1e-5`.
- Tensor ops only; no Python loops over rows or columns.

## Hints

1. What does `nn.Module.train()` actually change? Where does that flag live, and how does `forward` read it without you storing anything yourself?
2. `nn.Parameter` and `register_buffer` both store a tensor on the module. Which one is handed to the optimizer, which one is only saved and loaded, and which does each of `gamma`, `beta`, `running_mean`, `running_var` belong to?
3. In training mode two batches containing the same row produce different column means. Which quantity in eval mode plays the role of the column mean instead, and why does it not depend on the batch?
4. Updating a buffer with `self.running_mean = ...` replaces the registered tensor with a fresh one carrying autograd history. What in-place tensor method, under `torch.no_grad()`, keeps the buffer a buffer?

## Explain-back

- You train a model with BatchNorm, then serve it one request at a time without calling `model.eval()`. What happens on the first request, and what is wrong with the answers even when you batch a few requests together?
- Why is it right for training mode to use batch statistics even though it couples examples? What would go wrong if training used the running statistics from the start?
- After the first training batch, `running_mean` is only 10% of the way to the batch mean. How many batches until it mostly reflects the data, and what does this imply for evaluating a model after very few steps?
- List the four tensors this module stores and say, for each, whether gradient descent changes it. Which of them would you see in an optimizer's `param_groups`?
