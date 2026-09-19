# Stratified and time-series splits

Topic: 5. Train, validation, test, cross-validation and leakage
Difficulty: 2 of 3

## Problem

A plain random split fails in two common cases: a rare class that may barely show up in validation, and time-ordered data where the model must not train on the future. Write two pure-Python functions (no numpy):

- `stratified_split(labels: list, val_frac: float, seed: int) -> tuple[list[int], list[int]]` — split the row indices `0 … len(labels)−1` into `(train, val)` so that every class keeps its share. For each class separately, put `round(count · val_frac)` of its rows (chosen at random) into validation and the rest into training; each class's validation count must be within ±1 row of `count · val_frac`. Use one `random.Random(seed)` for all the randomness, so the same seed gives the same split, and a different seed a different one. Return both lists sorted ascending; together they hold every index exactly once. Labels are any hashable values. Raise `ValueError` if `labels` is empty or `val_frac` is not strictly between `0` and `1`.
- `time_series_splits(n: int, n_splits: int) -> list[tuple[list[int], list[int]]]` — expanding-window splits over rows `0 … n−1` that are already in time order. Let `test_size = n // (n_splits + 1)`. Split `i` (for `i = 0 … n_splits−1`) validates on the block starting at `start = n − (n_splits − i) · test_size` with `test_size` rows, and trains on every row before it: `train = [0, …, start−1]`, `val = [start, …, start + test_size − 1]`. Nothing is shuffled. Every validation index is later than every training index of its split, each training window contains the previous one, the validation blocks do not overlap, and the last one ends at row `n − 1`. The result matches `sklearn.model_selection.TimeSeriesSplit(n_splits).split(range(n))`. Raise `ValueError` if `n_splits < 1` or `n < n_splits + 1`.

## Examples

```
labels = [0] * 90 + [1] * 10
train, val = stratified_split(labels, 0.2, seed=0)
len(val), sum(labels[i] for i in val)           → (20, 2)       18 of class 0, 2 of class 1
stratified_split(labels, 1.0, seed=0)           → ValueError

time_series_splits(10, 3)
  → [([0, 1, 2, 3], [4, 5]),
     ([0, 1, 2, 3, 4, 5], [6, 7]),
     ([0, 1, 2, 3, 4, 5, 6, 7], [8, 9])]
time_series_splits(3, 3)                        → ValueError   test_size would be 0
```

## Constraints

- Pure Python: `random`, `collections` and `math` are allowed, numpy is not.
- Up to 100 000 rows; `stratified_split` is O(n log n) at most, `time_series_splits` O(n · n_splits).

## Hints

1. With 2% positives and a random 20% validation split of 1 000 rows, how many positives do you expect in validation, and how far can one unlucky seed move that number?
2. How do you collect the row indices of each class in one pass over `labels`?
3. For a time series, which rows does the model get to see when it is used in production, and what does a split need to imitate that?
4. For split `i`, where does the validation block start? Check your formula for the last split: where does its block end?

## Explain-back

- A classifier has 2% positives and you split randomly. What can go wrong with the validation score, and how does stratification fix it?
- Why is shuffling time-ordered data before splitting a form of leakage, even if no column mentions the future?
- The same patient appears in many rows. Neither of these splits handles that. What kind of split does, and what leaks without it?
- Why does the expanding window give later splits more training data, and what does that do to comparing their scores?
