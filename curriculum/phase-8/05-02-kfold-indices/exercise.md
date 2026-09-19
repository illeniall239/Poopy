# K-fold indices

Topic: 5. Train, validation, test, cross-validation and leakage
Difficulty: 2 of 3

## Problem

Write `kfold_indices(n: int, k: int) -> list[tuple[list[int], list[int]]]` in pure Python that returns the `k` folds of k-fold cross-validation over the row indices `0 … n−1`, as `(train_indices, val_indices)` pairs.

- The validation blocks are consecutive runs of indices, in order: fold 0 validates on the first block, fold 1 on the next, and so on. (Shuffle the rows beforehand if their order means something; this function does not shuffle.)
- Block sizes differ by at most one: every block has `n // k` indices, and the first `n % k` blocks get one extra. For `n = 10, k = 3` the sizes are `4, 3, 3`.
- Every index lands in exactly one validation block. Each fold's training indices are all the other indices, in ascending order. Train and validation of the same fold never share an index.
- The result matches `sklearn.model_selection.KFold(n_splits=k).split(range(n))` exactly.

Raise `ValueError` if `k < 2` or `k > n`.

## Examples

```
kfold_indices(5, 5)   → [([1, 2, 3, 4], [0]), ([0, 2, 3, 4], [1]), …, ([0, 1, 2, 3], [4])]    leave-one-out
kfold_indices(10, 3)  → [([4, 5, 6, 7, 8, 9], [0, 1, 2, 3]),
                         ([0, 1, 2, 3, 7, 8, 9], [4, 5, 6]),
                         ([0, 1, 2, 3, 4, 5, 6], [7, 8, 9])]
kfold_indices(4, 1)   → ValueError
kfold_indices(3, 4)   → ValueError
```

## Constraints

- Pure Python, no imports needed.
- `n` up to 100 000 and `k` up to `n`; the output is O(n · k) indices, so build each fold directly from ranges, not by filtering with `not in` over a list.

## Hints

1. With `n = 10` and `k = 3`, cutting at multiples of `n // k = 3` gives blocks of 3, 3, 3. Which index is left over, and where must the extra rows go?
2. If you know each block's size, how do you get each block's start position without floating-point division?
3. The training set for a fold is "everything except the block". How can you write that as two ranges instead of testing membership for every index?
4. When `k = n`, what does each fold look like, and what is that procedure usually called?

## Explain-back

- What does the average of the `k` validation scores estimate, and why is it more reliable than one holdout score?
- k-fold costs `k` trainings. When would you choose `k = 5` over leave-one-out, and when is a single holdout enough?
- Your folds skip index `n − 1` because of an off-by-one. What does that row never do, and would the averaged score reveal the bug?
- You fit the scaler once on all rows, then cross-validate. What leaked into each validation fold, and where should the fit happen?
