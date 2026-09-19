# Torch MLP matches micrograd

Topic: 7. PyTorch fundamentals: tensors, autograd, nn.Module, the training loop
Difficulty: 2 of 3

## Problem

Port the scalar-autograd MLP from Topic 4 to PyTorch and check that autograd gives the gradients you would compute by hand. Use `torch` (`nn.Module`, `nn.Linear`, autograd). All tensors and parameters are `torch.float64`.

- `class MLP(nn.Module)` with `__init__(self, sizes)`. `sizes` lists the layer widths starting with the input, e.g. `[2, 2, 1]`. Build one `nn.Linear(sizes[i], sizes[i + 1], dtype=torch.float64)` per consecutive pair and store them in `self.layers`, an `nn.ModuleList`, in order. `forward(x)` applies the layers in order with `tanh` after every layer **except the last** (the output is raw). `x` has shape `(N, sizes[0])`; the output has shape `(N, sizes[-1])`. Raise `ValueError` if `sizes` has fewer than 2 entries.
- `load_weights(model, weights)` copies given numbers into the model's parameters, in place. `weights` is a list with one `(W, b)` pair per layer, as nested Python lists: `W` has shape `(out, in)` (the `nn.Linear` layout, one row per output unit) and `b` has shape `(out,)`. After loading, the parameters must still be the same `nn.Parameter` objects, still leaf tensors with `requires_grad=True`. Do not use `.data`; do the copy under `torch.no_grad()`. Raise `ValueError` if the number of pairs or any shape does not match the model.
- `loss_and_grads(model, X, y)` computes the mean squared error `mean((model(X) − y)²)` over all elements, runs backward, and returns `(loss, grads)`: `loss` as a Python `float`, `grads` a list of tensors, one per parameter in `model.parameters()` order (`W1, b1, W2, b2, …`), each a copy of that parameter's gradient. Calling it twice in a row on the same data must return the same gradients both times.

## Examples

```
model = MLP([2, 2, 1])
load_weights(model, [([[0.5, -0.5], [0.25, 1.0]], [0.0, 0.1]),
                     ([[1.0, -1.0]], [0.5])])
model(torch.tensor([[1.0, 2.0]], dtype=torch.float64))
    → [[-0.94409056]]
         hidden = tanh([-0.5, 2.35]) = [-0.46211716, 0.9819734]
         out = -0.46211716 - 0.9819734 + 0.5

loss, grads = loss_and_grads(model, torch.tensor([[1.0, 2.0]], dtype=torch.float64),
                                    torch.tensor([[0.0]], dtype=torch.float64))
loss      → 0.89130699
grads[2]  → [[0.87256089, -1.85414364]]      dW2 = 2(out − y) · hidden
grads[3]  → [-1.88818112]                    db2 = 2(out − y)
grads[1]  → [-1.48495576, 0.06746138]        db1 = 2(out − y) · W2 · (1 − hidden²)
```

## Constraints

- `torch` on CPU, float64 throughout.
- Networks have at most 5 layers of width at most 64; batches have at most 100 rows.
- Gradients match a hand-written backward pass within `1e-10`.

## Hints

1. Why does `nn.ModuleList` register the layers' parameters with the model when a plain Python list does not? How can you check that it worked?
2. `nn.Linear` stores its weight as `(out, in)` and computes `x @ W.T + b`. How does that match the layout of `weights`?
3. Replacing `layer.weight` with a new tensor and copying new values into the existing one are different things. Which one keeps the optimizer and autograd pointing at the right object, and why does the copy need `torch.no_grad()`?
4. `.backward()` adds into `.grad`; it does not overwrite it. What must happen before each backward so a second call returns the same gradients, and why should you return copies rather than the `.grad` tensors themselves?

## Explain-back

- Your `loss_and_grads` clears gradients before backward. What would the second call return if it did not, and how does that map to forgetting `optimizer.zero_grad()` in a training loop?
- Why is writing through `.data` to get around an in-place error dangerous, compared with `torch.no_grad()` and `copy_`?
- For the example, derive `db1` by hand. Where do the factors `2(out − y)`, `W2` and `1 − tanh²` come from, and which one is the local gradient of the activation?
- What changes in this code if the model contains dropout or BatchNorm and you want the gradients to match a hand computation?
