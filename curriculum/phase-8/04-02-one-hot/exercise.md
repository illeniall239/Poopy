# One-hot encoding and buckets

Topic: 4. Features: scaling, encoding and feature engineering
Difficulty: 2 of 3

## Problem

Turn categories and numbers into model-ready columns. Write two pure-Python functions (no numpy):

- `one_hot(values: list[str], vocabulary: list[str]) -> list[list[int]]` — one row per value, with `len(vocabulary) + 1` columns. Column `i` is `1` when the value equals `vocabulary[i]`; the final column is the **unknown bucket**, `1` for any value not in the vocabulary. Every row has exactly one `1`. The column order is the vocabulary's order, whatever order the values arrive in, so the same vocabulary always gives the same columns. Matching is exact (case-sensitive). Raise `ValueError` if the vocabulary contains a duplicate. An empty `values` list gives `[]`.
- `bucketize(x: float, boundaries: list[float]) -> int` — the index of the bucket `x` falls in, for strictly increasing `boundaries`: `0` if `x < boundaries[0]`, `i` if `boundaries[i−1] ≤ x < boundaries[i]`, and `len(boundaries)` if `x ≥ boundaries[-1]`. A value exactly on a boundary goes to the bucket above it. Raise `ValueError` if `boundaries` is empty or not strictly increasing.

The vocabulary and the boundaries are decided from training data (or by hand) before encoding; nothing here looks at the values to change the columns.

## Examples

```
one_hot(["red", "blue", "green", "red"], ["blue", "red"])
    → [[0, 1, 0], [1, 0, 0], [0, 0, 1], [0, 1, 0]]     "green" goes to the unknown bucket
one_hot(["Red"], ["blue", "red"])        → [[0, 0, 1]]
one_hot([], ["a"])                       → []
one_hot(["a"], ["a", "b", "a"])          → ValueError
bucketize(5, [10, 20, 30])               → 0
bucketize(10, [10, 20, 30])              → 1          on a boundary: the bucket above
bucketize(25, [10, 20, 30])              → 2
bucketize(99, [10, 20, 30])              → 3
bucketize(1, [3, 2])                     → ValueError
```

## Constraints

- Pure Python: `bisect` and `collections` are allowed, numpy is not.
- `values` up to 10 000 and `vocabulary` up to 1 000. The output alone is `len(values) × (len(vocabulary) + 1)`; finding a value's column must be an O(1) lookup, not a scan of the vocabulary.
- `bucketize` is O(log len(boundaries)).

## Hints

1. What should the model receive at inference time for a category that did not exist in training, and what happens if there is no column for it?
2. How can you find a value's column position in constant time instead of calling `vocabulary.index(value)`?
3. Why is "red = 0, blue = 1, green = 2" a worse input for linear regression than three 0/1 columns, even though it is shorter?
4. The `bisect` module has a left and a right variant. For a value exactly equal to a boundary, which one returns the bucket above?

## Explain-back

- Your model maps city to 0, 1, 2, … and feeds it to linear regression. What relationship between cities did you just tell the model exists?
- A user-ID column has 10 000 000 distinct values. Why is a one-hot column per ID a bad idea, and what would you do instead?
- Why must the vocabulary come from the training rows only, and what does the unknown bucket protect you from in production?
- Age bucketed into decades lets a linear model do something raw age does not. What is it?
