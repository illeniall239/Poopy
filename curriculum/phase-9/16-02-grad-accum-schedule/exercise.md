# Gradient accumulation schedule

Topic: 16. GPUs, performance and debugging training
Difficulty: 1 of 3

## Problem

A batch of 64 does not fit in memory, but 16 does. Gradient accumulation runs several small *micro-batches*, calls `backward()` on each (PyTorch adds the gradients up in `.grad`), and only then calls `optimizer.step()` and `zero_grad()`. Plan that loop in plain Python (no numpy, no torch).

`grad_accum_schedule(micro_batches, accum)` takes the number of micro-batches in the epoch (indexed `0 … micro_batches − 1`) and how many micro-batches to accumulate per optimizer step. It returns a tuple `(step_at, scale)`:

- `step_at` is the sorted `list[int]` of micro-batch indices right after which `step()` runs: after every `accum`-th micro-batch, **and** after the last micro-batch of the epoch if a partial group is left over, so no gradient is silently carried into the next epoch.
- `scale` is the `float` each micro-batch loss is multiplied by before `backward()` so that a full group of `accum` equal-sized micro-batches produces the same gradient as one big batch whose loss is the **mean** over all its examples.

Raise `ValueError` if `micro_batches < 1` or `accum < 1`.

## Examples

```
grad_accum_schedule(8, 4)   → ([3, 7], 0.25)
grad_accum_schedule(10, 4)  → ([3, 7, 9], 0.25)       the last group has only 2 micro-batches
grad_accum_schedule(3, 1)   → ([0, 1, 2], 1.0)        accum = 1 is ordinary training
grad_accum_schedule(2, 5)   → ([1], 0.2)
grad_accum_schedule(0, 4)   → ValueError
```

## Constraints

- `micro_batches` and `accum` are ints up to 10⁶.
- Plain Python only.

## Hints

1. Counting from 0, after which micro-batch does the first group of `accum` end? The second?
2. What condition on the index `i` says "this micro-batch closes a group"?
3. What must happen at the very last index if it does not close a full group, and how do you avoid listing it twice when it does?
4. If each micro-batch loss is already a mean over its own examples and `.grad` *sums* across `backward()` calls, what factor turns that sum into a mean over the whole group?

## Explain-back

- Why does the loss need scaling at all? What goes wrong with the effective learning rate if you forget it?
- Your leftover group at the end of an epoch is smaller than `accum`, but still uses the same `scale`. Is its gradient then a true mean? Is that a problem worth fixing?
- Is accumulating 4 micro-batches of 16 exactly the same as one batch of 64 for a model with BatchNorm? Why or why not?
- What does gradient accumulation save, memory or time? What does it cost?
