# Train, validation and test split

Topic: 5. Train, validation, test, cross-validation and leakage
Difficulty: 1 of 3

## Problem

Write `train_val_test_split(n: int, fracs: tuple[float, float, float], seed: int) -> tuple[list[int], list[int], list[int]]` in pure Python that splits the row indices `0 … n−1` into train, validation and test index lists.

- `fracs = (train_frac, val_frac, test_frac)`: three numbers, each `≥ 0`, summing to `1` within `1e-9`.
- Shuffle `order = list(range(n))` with `random.Random(seed).shuffle(order)`.
- Cut the shuffled order at `c1 = round(n · train_frac)` and `c2 = round(n · (train_frac + val_frac))`: train is `order[:c1]`, validation `order[c1:c2]`, test `order[c2:]`. Cutting at cumulative points means the three sizes always add up to `n`, with no index lost or repeated to rounding.
- The three lists are disjoint and together hold every index exactly once. The same `seed` gives the same split; a different seed gives a different one.
- `n = 0` returns three empty lists.

Raise `ValueError` if `n < 0`, if `fracs` does not have exactly three entries, if any fraction is negative, or if they do not sum to `1` within `1e-9`.

## Examples

```
train, val, test = train_val_test_split(10, (0.6, 0.2, 0.2), seed=0)
len(train), len(val), len(test)                   → (6, 2, 2)
sorted(train + val + test)                        → [0, 1, 2, …, 9]
train_val_test_split(10, (0.6, 0.2, 0.2), seed=0) → the same three lists again
train_val_test_split(7, (0.5, 0.25, 0.25), 1)     → sizes (4, 1, 2)       c1 = round(3.5) = 4, c2 = round(5.25) = 5
train_val_test_split(5, (0.5, 0.5, 0.5), 0)       → ValueError            sums to 1.5
```

## Constraints

- Pure Python: `random` and `math` are allowed, numpy is not.
- `n` up to 1 000 000; O(n).
- Use exactly the shuffle and cut points above (Python's built-in `round`), so the tests can reproduce your split.

## Hints

1. What is each of the three sets for, and which one may you look at only once, at the very end?
2. If you round each of the three sizes separately, can they add up to `n − 1` or `n + 1`? How do cumulative cut points avoid that?
3. Why shuffle before cutting, and when would shuffling be the wrong thing to do?
4. Where does the randomness come from, and what must you pass to it so a teammate gets the same split tomorrow?

## Explain-back

- You tried 40 hyperparameter settings and picked the best by its test score. Why is that score no longer a test score, and what should you have used?
- The rows are daily sales ordered by date. What is wrong with a random split here, and what split would you use instead?
- The same customer appears in 30 rows. What can go wrong when some of their rows land in train and others in test?
- Why fix the seed for a split, and why is it still worth trying a second seed before trusting a small difference between two models?
