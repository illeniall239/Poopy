# Choose k by cross-validation

Topic: 10. k-nearest neighbors
Difficulty: 3 of 3

## Problem

k is a hyperparameter: pick it with k-fold cross-validation on the training data, never on the test set. Write two NumPy functions. `X` has shape `(n, d)`, `y` holds `n` integer labels, `folds` is the number of folds.

- `cv_accuracy(X: np.ndarray, y: np.ndarray, k: int, folds: int) -> float` — the mean validation accuracy of kNN over `folds` folds, as a Python `float`.
- `choose_k(X: np.ndarray, y: np.ndarray, ks: list[int], folds: int) -> int` — the `k` in `ks` with the highest `cv_accuracy`. If several tie, return the **smallest** of them (the simpler, smoother model). `ks` may be in any order.

**How the folds are formed** (the Topic 5 k-fold, re-implemented here): the rows are **not shuffled**. Validation folds are contiguous blocks of indices in order. With `q, r = divmod(n, folds)`, the first `r` folds have `q + 1` rows and the rest have `q`, so sizes differ by at most one and every index lands in exactly one validation fold. For `n = 10, folds = 3` the validation folds are `[0..3]`, `[4..6]`, `[7..9]`. Each fold's training set is every other row, **kept in original index order**.

**How kNN predicts** (the rules from `10-01-knn-classify`), for each validation row against its fold's training rows:

1. Euclidean distance; order training rows by distance, equal distances broken by the smaller position in the training set (which, since training rows keep their original order, is the smaller original index). Take the first `k`.
2. Majority vote; among labels tied for the most votes, the one whose closest member among the `k` is nearest; if still tied, the smallest label.

A fold's accuracy is the fraction of its validation rows predicted correctly; `cv_accuracy` is the plain mean of the `folds` accuracies (not weighted by fold size).

Raise `ValueError` if `folds < 2` or `folds > n`, if `ks` is empty, or if any `k` is below 1 or larger than the smallest training set (`n − (q + 1)` when `r > 0`, else `n − q`).

## Examples

```
X = [[0.0], [0.1], [0.2], [5.0], [5.1], [5.2]], y = [0, 0, 0, 1, 1, 1]
folds = 3 → validation folds [0, 1], [2, 3], [4, 5]
cv_accuracy(X, y, 1, 3)          → 1.0
cv_accuracy(X, y, 3, 3)          → 0.3333   folds [0, 1] and [4, 5] leave only one row of their own class in training
choose_k(X, y, [3, 2, 1], 3)     → 1        k = 1 and k = 2 both score 1.0: the smaller wins
choose_k(X, y, [5], 3)           → ValueError   every training set has only 4 rows
```

## Constraints

- NumPy allowed. For each fold you may compute the full `(validation × training)` distance matrix at once.
- `n` up to 1000, `d` up to 20, up to 10 folds and 10 values of k; the whole search finishes in a couple of seconds.
- Accuracies within `1e-12` of the tests' expected values.

## Hints

1. Before any kNN: write the fold boundaries for `n = 10, folds = 3` by hand. Which folds get the extra row, and how do you turn sizes into start and stop indices?
2. How do you build a fold's training set from the rows before and after its validation block while keeping their order?
3. You evaluate every k on the same folds. Which work (distances, sorted neighbor order) can be shared across all the k values instead of recomputed?
4. When two ks score the same, why prefer the smaller one here, and how do you make the choice independent of the order of `ks`?

## Explain-back

- Why pick k on cross-validation folds rather than on the test set? What would the test score mean afterwards?
- k = 1 has zero training error. What does cross-validation show about it on noisy labels, and why?
- Why must every index land in exactly one validation fold? What goes wrong if folds overlap or skip a row?
- Here folds are not shuffled. When is that correct, and when (say, rows sorted by label) does it give a misleading score?
