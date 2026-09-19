# Random search

Topic: 20. The practical workflow: a scikit-learn-style capstone
Difficulty: 2 of 3

## Problem

Random search samples `n` configurations instead of trying every combination, and it can sample continuous ranges. Write one pure-Python function:

`random_search(space: dict, n: int, rng: random.Random) -> list[dict]`

Each value in `space` describes how to sample one hyperparameter:

- a **list** of values: pick one with `rng.choice(values)`;
- the tuple `("uniform", low, high)`: `rng.uniform(low, high)`;
- the tuple `("loguniform", low, high)`: sample uniformly in log space, `math.exp(rng.uniform(math.log(low), math.log(high)))`. Use this for learning rates and regularization strengths, whose useful values span several orders of magnitude.

Return `n` configuration dicts. To make a run reproducible from its seed, the calls to `rng` happen in a fixed order: configurations are built one after another, and within each configuration the names are sampled in alphabetical order, one `rng` call each, exactly as written above.

Raise `ValueError` (before drawing anything) if `n < 0`; if a list is empty; if a tuple is not exactly `(kind, low, high)` with `kind` either `"uniform"` or `"loguniform"` and `low < high`; if a `"loguniform"` range has `low <= 0`; or if a value is neither a list nor such a tuple. `n = 0` returns `[]`.

## Examples

```
space = {"lr": ("loguniform", 1e-5, 1e-1), "depth": [2, 4, 8], "dropout": ("uniform", 0.0, 0.5)}
random_search(space, 2, random.Random(0))
    → two dicts with keys depth, dropout, lr; the same two dicts every time for seed 0
random_search(space, 0, random.Random(0))                      → []
random_search({"lr": ("loguniform", 0.0, 1.0)}, 5, random.Random(0))  → ValueError   log of 0
random_search({"lr": ("normal", 0.0, 1.0)}, 5, random.Random(0))      → ValueError
```

## Constraints

- Pure Python: `math` and `random` are allowed. Use only the `rng` passed in, never the global `random` functions.
- `n` up to 100 000.

## Hints

1. Which `random.Random` method matches each of the three kinds of value, and how many calls does each configuration make?
2. If you iterate over `space` in insertion order, how could two people with the same seed get different configurations?
3. Between `1e-5` and `1e-1`, what fraction of plain uniform samples fall below `1e-3`? What fraction of log-uniform samples do?
4. Why should every check happen before the first draw, and not halfway through building the list?

## Explain-back

- Why does log-uniform sampling suit a learning rate, and what goes wrong with a uniform range from `1e-5` to `1e-1`?
- With the same budget of 60 runs, why does random search often beat a grid when only one or two hyperparameters matter?
- Your best of 2 000 random configurations scored 0.94 on validation. What test score do you expect, and why lower?
- A colleague reruns your search and gets different configurations. List what must be fixed for the run to be reproducible.
