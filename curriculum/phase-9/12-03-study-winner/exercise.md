# Study winner

Topic: 12. Hyperparameter tuning methodology and experiment tracking
Difficulty: 2 of 3

## Problem

In the Tuning Playbook a **study** asks one question about one **scientific** hyperparameter, for example "which optimizer is best?". Every other hyperparameter that must be retuned for a fair comparison (usually the learning rate) is a **nuisance** parameter: each scientific value gets its own nuisance sweep, and each value is judged by its **best** run, not its average, because a bad learning rate says nothing about the optimizer. Write `study_winner(runs, scientific_param, metric)` in plain Python.

- `runs` is a list of dicts shaped `{"config": {...}, "steps": int, "metrics": {...}}`. `config` always contains `scientific_param`. `metrics` holds final values where **lower is better** (a loss or an error rate).
- A run whose `metrics` lacks `metric`, or whose value is `NaN` (a diverged run), is skipped.
- For every value of `scientific_param`, pick its best run: the lowest `metric`; among equal metrics, the run with the fewest `steps`; if still tied, the one that comes first in `runs`.
- The winner is the scientific value whose best run is best by the same rule (lowest metric, then fewest steps, then the value whose best run comes first in `runs`).
- Return `(winner, table)` where `table` maps every scientific value that has at least one usable run to its best run's metric value.

Raise `ValueError` if no run is usable (including an empty `runs`). Values of the scientific parameter may be any hashable type.

## Examples

```
runs = [
  {"config": {"opt": "sgd",  "lr": 0.1},   "steps": 1000, "metrics": {"val_loss": 0.50}},
  {"config": {"opt": "sgd",  "lr": 0.01},  "steps": 1000, "metrics": {"val_loss": 0.40}},
  {"config": {"opt": "adam", "lr": 0.01},  "steps": 1000, "metrics": {"val_loss": 0.90}},
  {"config": {"opt": "adam", "lr": 0.001}, "steps": 1000, "metrics": {"val_loss": 0.35}},
]
study_winner(runs, "opt", "val_loss")  → ("adam", {"sgd": 0.40, "adam": 0.35})
   (by average sgd 0.45 would beat adam 0.625: the wrong answer)

Two values tied at 0.3, reached in 800 vs 500 steps → the one that took 500 steps wins.
study_winner([], "opt", "val_loss")  → ValueError
```

## Constraints

- At most 10 000 runs.
- Plain Python (`math.isnan` is fine).

## Hints

1. Why does averaging a scientific value's runs over its learning-rate sweep punish it for learning rates that were simply wrong for it?
2. What should a run that diverged to `NaN` contribute to the comparison, and what does `nan < 0.4` evaluate to?
3. How can a tuple such as `(metric, steps)` express "lowest metric, then fewest steps" in a single comparison?
4. If you keep, for each scientific value, only the best run seen so far and replace it only on a strictly better key, which tie rule do you get for free?

## Explain-back

- You changed the optimizer *and* the learning rate range between two studies and the second is better. Which change gets the credit?
- Why take the best over the nuisance parameters instead of fixing the learning rate at one value for every optimizer?
- What is the difference between a scientific, a nuisance and a fixed hyperparameter? Give one example of each.
- The two best values differ by 0.002 from one seed each. What would you do before declaring a winner?
