# Minibatches

Topic: 3. Gradient descent for linear regression
Difficulty: 2 of 3

## Problem

Minibatch gradient descent needs, every epoch, a fresh shuffled order of the rows cut into batches. Write a generator with NumPy:

`minibatches(n: int, batch_size: int, rng: np.random.Generator) -> Iterator[list[int]]`

- Draw one shuffled order of the indices `0 … n−1` from `rng` (for example with `rng.permutation(n)`) per call, and yield consecutive slices of it as lists of Python `int`.
- Every batch has exactly `batch_size` indices except the last, which holds whatever is left (`1 … batch_size` indices). Across one call every index appears exactly once: none skipped, none repeated.
- `n = 0` yields nothing. A `batch_size` larger than `n` yields one batch with all `n` indices.
- Raise `ValueError` if `n < 0` or `batch_size < 1`. Raise it when `minibatches` is called, not only when iteration starts. The body of a function containing `yield` does not run until the first `next()`, so `minibatches` itself should be a plain function that validates and then returns a generator (a generator expression or an inner generator function).
- The randomness comes only from `rng`: two generators with the same seed give the same batches, and calling `minibatches` twice with the same `rng` object (two epochs) gives two different orders.

## Examples

```
rng = np.random.default_rng(0)
list(minibatches(10, 4, rng))    → e.g. [[6, 2, 7, 4], [5, 0, 1, 9], [8, 3]]   sizes 4, 4, 2
list(minibatches(3, 10, rng))    → one batch holding 0, 1, 2 in some order
list(minibatches(0, 4, rng))     → []
minibatches(10, 0, rng)          → ValueError
```

## Constraints

- NumPy allowed (and needed for the generator argument).
- `n` up to 1 000 000: O(n) per call, no Python loop over pairs of indices.
- Batches are lists of built-in `int`, not NumPy arrays.

## Hints

1. If you shuffle once before the first epoch and reuse that order, what do the gradients of consecutive epochs have in common?
2. How many batches are there for `n` rows and batch size `b`? Write it without floats.
3. What does a slice `order[start:start + b]` give you when `start + b` runs past the end, and does that make the short last batch free?
4. A generator function's body does not run until the first `next()`. Where must a validation check live so the error appears at the call?

## Explain-back

- Why shuffle every epoch instead of once? What can go wrong if the data is sorted by label or by date and never shuffled?
- A loop builds batches with `range(0, n - batch_size, batch_size)`. Which rows does it skip, and how would you notice from the training results?
- Stochastic, minibatch and full-batch descent differ only in `batch_size`. What values give each, and what does each trade off?
- Why is a noisy minibatch loss curve normal, and what would you look at to decide whether training is still improving?
