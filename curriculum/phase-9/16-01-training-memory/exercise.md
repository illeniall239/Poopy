# Training memory

Topic: 16. GPUs, performance and debugging training
Difficulty: 1 of 3

## Problem

Before you rent a GPU, estimate whether the model even fits. Write two functions in plain Python (no numpy, no torch). Throughout, **1 MB means 1024 × 1024 bytes**, and results are returned as a `float` without rounding.

- `param_memory_mb(n_params, dtype)` returns the memory, in MB, needed to store `n_params` numbers of type `dtype`. `dtype` is one of the strings `"float64"` (8 bytes), `"float32"` (4 bytes), `"float16"` (2 bytes) and `"bfloat16"` (2 bytes). Raise `ValueError` for any other `dtype` string and for a negative `n_params`.
- `adam_training_memory_mb(n_params)` returns the memory, in MB, that plain float32 training with Adam needs for the model's *state*: the weights, one gradient per weight, and Adam's two moment buffers (first and second moment), all float32. Raise `ValueError` for a negative `n_params`. Activations are **not** counted: they depend on the batch size and the architecture, not only on the parameter count.

## Examples

```
param_memory_mb(1_048_576, "float32")   → 4.0
param_memory_mb(1_048_576, "bfloat16")  → 2.0
param_memory_mb(0, "float16")           → 0.0
param_memory_mb(10, "int8")             → ValueError
adam_training_memory_mb(1_048_576)      → 16.0      weights + grads + m + v, 4 bytes each
adam_training_memory_mb(7_000_000_000)  → 106811.5234375   a 7B model: about 104 GB before any activations
```

## Constraints

- `n_params` is an `int` between 0 and 10¹².
- Plain Python only.

## Hints

1. How many bytes does one number of each dtype take? Where could you keep that mapping so an unknown dtype is easy to detect?
2. How do you turn a byte count into MB when 1 MB is 1024 × 1024 bytes?
3. For every weight, which other float32 numbers must live in memory while Adam trains: how many copies of "one number per parameter" are there?
4. Can `adam_training_memory_mb` reuse `param_memory_mb` instead of repeating the arithmetic?

## Explain-back

- Your Adam estimate ignores activations. Which knob makes activation memory grow, and why does it not change the parameter count?
- float16 and bfloat16 both take 2 bytes. What does each give up compared to float32, and why is bfloat16 less prone to overflow?
- A training run is slow because the GPU sits idle waiting for batches. Will a bigger GPU help? What would you change instead?
- Calling `model.to(device)` moved the weights. Does it move your input batches too? What happens if you forget?
