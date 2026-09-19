# Log-uniform random search

Topic: 12. Hyperparameter tuning methodology and experiment tracking
Difficulty: 2 of 3

## Problem

Random search draws each trial's hyperparameters independently from a search space. For a learning rate between `1e-5` and `1e-1`, every **factor of ten** matters equally, so it must be sampled uniformly in `log` space, not uniformly between the two numbers. Write `sample_configs(space, n, rng)` in plain Python (the `math` module is fine).

`space` maps each hyperparameter name to a spec tuple:

- `("log", low, high)` — a float drawn log-uniformly: `exp(u)` with `u` uniform between `log(low)` and `log(high)`. Requires `0 < low < high`.
- `("uniform", low, high)` — a float drawn uniformly between `low` and `high`. Requires `low < high`.
- `("choice", options)` — one element of the non-empty list `options`, each equally likely.

`rng` is a `random.Random`; use only it (e.g. `rng.uniform`, `rng.choice`) so that the same seed gives the same configs. Return a list of `n` dicts, each with exactly the keys of `space`. `n = 0` returns `[]`.

Raise `ValueError` for an unknown spec kind, for `low`/`high` that break the rules above, for an empty `options` list, or for `n < 0`. A bad `space` raises even when `n` is `0`.

## Examples

```
space = {"lr": ("log", 1e-5, 1e-1), "dropout": ("uniform", 0.0, 0.5), "opt": ("choice", ["sgd", "adam"])}
sample_configs(space, 2, random.Random(0))  → [{"lr": ..., "dropout": ..., "opt": ...}, {...}]
sample_configs(space, 0, random.Random(0))  → []

With 2000 samples of ("log", 1e-5, 1e-1):
  about a quarter land in each decade [1e-5, 1e-4), [1e-4, 1e-3), [1e-3, 1e-2), [1e-2, 1e-1]
  about half are below 1e-3, the geometric midpoint
(uniform sampling would put about 90 % in the top decade)

sample_configs({"lr": ("log", 0.0, 1.0)}, 1, rng)  → ValueError
```

## Constraints

- `n` is at most 10 000; `space` has at most 20 entries.
- Tests check each decade gets between 20 % and 30 % of 2000 log-uniform samples.

## Hints

1. If you draw `lr` uniformly from `[1e-5, 1e-1]`, what fraction of draws is below `1e-3`? Is that what you want when each decade is equally plausible?
2. Which transformation turns "equal chance per factor of ten" into "equal chance per unit length"?
3. After drawing `u` uniformly in the transformed space, how do you map it back?
4. Where should the validation of each spec happen so that a bad space fails even when `n` is `0`?

## Explain-back

- Why is a learning rate sampled log-uniformly while a dropout rate is usually sampled uniformly?
- Why does random search usually beat a grid with the same number of trials when only one or two hyperparameters really matter?
- You sweep the learning rate and the batch size together and the best run has the largest batch. What can and can't you conclude?
- You found the best config on the test set. What went wrong, and what should you have used?
