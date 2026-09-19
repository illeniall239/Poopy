# Bootstrap and bagging

Topic: 12. Ensembles: bagging, random forests and gradient boosting
Difficulty: 1 of 3

## Problem

Bagging trains many models, each on its own bootstrap resample of the training rows, and combines their predictions. Write two pure-Python functions:

- `bootstrap_sample(n: int, rng: random.Random) -> tuple[list[int], list[int]]` returns `(in_bag, out_of_bag)`. `in_bag` holds `n` row indices drawn **with replacement**, made by exactly `[rng.randrange(n) for _ in range(n)]` so that a given seed always gives the same sample (the test replays that call). `out_of_bag` is the sorted list of indices in `range(n)` that never appear in `in_bag`. Raise `ValueError` if `n < 1`.
- `bagged_predict(models: list, x, mode: str = "vote")` calls every model as `model(x)` and combines the answers. With `mode="vote"` it returns the most common prediction, a tie going to the smallest value. With `mode="mean"` it returns the mean of the predictions as a float. Raise `ValueError` if `models` is empty or `mode` is anything else.

A model here is any callable that takes one row and returns a label or a number, so `bagged_predict` works for trees, stumps or lambdas alike.

## Examples

```
rng = random.Random(0)
bootstrap_sample(5, rng)     → ([3, 3, 0, 2, 4], [1])       with replacement: 3 twice, 1 left out
bootstrap_sample(0, rng)     → ValueError

models = [lambda x: "cat", lambda x: "dog", lambda x: "cat"]
bagged_predict(models, [1.0])                      → "cat"
bagged_predict([lambda x: 2, lambda x: 1], None)   → 1        a tie goes to the smallest
bagged_predict([lambda x: 1.0, lambda x: 4.0], None, mode="mean")   → 2.5
```

## Constraints

- Pure Python: `random`, `collections` and `statistics` are allowed, numpy is not.
- `n` ≤ 100 000; `bootstrap_sample` is O(n).
- Use only `rng` for randomness; never the module-level `random` functions.

## Hints

1. If you drew `n` indices without replacement, what would every sample be, and why would every model trained on it be the same?
2. With replacement, some indices appear twice and some not at all. What is a cheap way to find the ones that never appeared?
3. About what fraction of the rows do you expect to be out of bag for large `n`? Work out the chance that one particular row is missed by all `n` draws.
4. For a vote, how do you count predictions, and among the labels that share the top count, how do you pick one deterministically?

## Explain-back

- Why must a bootstrap sample be drawn with replacement, and what fraction of rows ends up out of bag (roughly `1/e`)?
- How can the out-of-bag rows serve as a validation set without holding out any data?
- Averaging `B` models each with variance `σ²` gives variance `σ²/B` only if they are independent. Why are bagged trees not independent, and what does that do to the benefit?
- Why does bagging help a deep tree a lot but a linear regression almost not at all?
