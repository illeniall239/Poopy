# Ablation table

Topic: 19. Capstone: a tiny CNN and a character-level LM from scratch
Difficulty: 1 of 3

## Problem

An ablation changes one thing at a time (init, normalization, dropout, optimizer) and compares each run against a baseline. The comparison only means something if everything else, including the seed, stayed the same. Write the table in plain Python (no numpy, no torch).

Each run is a dict:

```
{"name": "no-dropout", "seed": 0, "metrics": {"val_loss": 1.91, "val_acc": 0.62}}
```

`ablation_table(runs, baseline)` takes the list of runs and the **name** of the baseline run and returns a `list` of dicts, one per run other than the baseline, in the same order as `runs`:

```
{"name": <run name>, "deltas": {<metric>: run value − baseline value, ...}, "seed_differs": <bool>}
```

- `deltas` has one entry for every metric of the baseline, and only those (extra metrics a run logged are ignored).
- `seed_differs` is `True` when the run's seed is not the baseline's seed: that row's delta mixes the change with seed noise and must not be trusted.
- Raise `ValueError` if no run has the baseline name, if two runs share a name, or if a run is missing one of the baseline's metrics.

## Examples

```
runs = [
  {"name": "base",       "seed": 0, "metrics": {"val_loss": 2.00, "val_acc": 0.60}},
  {"name": "no-dropout", "seed": 0, "metrics": {"val_loss": 2.25, "val_acc": 0.55}},
  {"name": "adamw",      "seed": 1, "metrics": {"val_loss": 1.90, "val_acc": 0.63, "train_loss": 1.2}},
]
ablation_table(runs, "base") →
  [{"name": "no-dropout", "deltas": {"val_loss": 0.25, "val_acc": -0.05}, "seed_differs": False},
   {"name": "adamw",      "deltas": {"val_loss": -0.10, "val_acc": 0.03}, "seed_differs": True}]

ablation_table(runs, "baseline")  → ValueError      no run with that name
ablation_table([runs[0]], "base") → []
```

Deltas are floats; the tests compare them with a tolerance of `1e-9`.

## Constraints

- Up to 1000 runs, each with up to 50 metrics.
- Plain Python only. Do not modify the input dicts.

## Hints

1. How do you find the baseline run by name, and how can you tell in the same pass whether two runs share a name?
2. Which dict decides the set of metrics in `deltas`: the baseline's or each run's?
3. What is the sign convention: is a positive `val_loss` delta good or bad news for that change?
4. What single comparison decides `seed_differs`, and why is it worth putting in the table rather than leaving to the reader?

## Explain-back

- Run "adamw" is 0.10 better on validation loss but used seed 1. What must you do before you can claim AdamW helped, and how big could seed noise alone be?
- Why does the table report validation metrics and not training loss? What would a training-loss-only table hide?
- Why must the ablation never be scored on the test split, even though it is "just a comparison"?
- Two changes each improve the loss by 0.1 alone. Will doing both improve it by 0.2? What does that say about changing one thing at a time?
