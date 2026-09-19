# Run log

Topic: 12. Hyperparameter tuning methodology and experiment tracking
Difficulty: 2 of 3

## Problem

A result you cannot reproduce is not a result. An experiment record is the config, the seed, the code version and the metrics at every step. Tools like MLflow and W&B are, at heart, a table of these records. Write a `RunLog` class in plain Python that keeps one.

- `RunLog()` starts empty.
- `start(name, config, seed, code_version)` records a new run. `config` is a dict of hyperparameters; store a **copy**, so changing the caller's dict later does not change the record. `code_version` is a string such as a git commit hash. Raise `ValueError` if a run with that `name` already exists, or if `config` has a key named `"seed"` or `"code_version"`.
- `log(name, step, metrics)` records a dict of metric values (floats) for run `name` at integer `step`. Raise `KeyError` if the run was never started. Raise `ValueError` if `step` is not strictly greater than the previous step logged for that run. A call may log any subset of metrics.
- `best(metric, mode="min")` looks at every value of `metric` logged by any run at any step and returns `(run_name, step, value)` for the lowest one (`mode="min"`) or the highest (`mode="max"`). Ties go to the run started first, then the earlier step. Raise `KeyError` if no run ever logged `metric`, and `ValueError` if `mode` is not `"min"` or `"max"`.
- `compare(a, b)` returns a dict with two entries:
  - `"changed"`: `{key: (value_in_a, value_in_b)}` for every config key whose values differ, plus `"seed"` and `"code_version"` when those differ. A key missing from one run's config counts as the value `None` there.
  - `"deltas"`: `{metric: last_b - last_a}` for every metric both runs logged, where `last` is the value at the last step that metric was logged.

  Raise `KeyError` if either run does not exist.

## Examples

```
log = RunLog()
log.start("base", {"lr": 0.1, "bs": 32}, seed=0, code_version="a1b2c3")
log.start("lr01", {"lr": 0.01, "bs": 32}, seed=0, code_version="a1b2c3")
log.log("base", 1, {"val_loss": 0.9, "acc": 0.6})
log.log("base", 2, {"val_loss": 0.7, "acc": 0.7})
log.log("lr01", 1, {"val_loss": 0.8})
log.log("lr01", 2, {"val_loss": 0.5})

log.best("val_loss")          → ("lr01", 2, 0.5)
log.best("acc", mode="max")   → ("base", 2, 0.7)
log.compare("base", "lr01")   → {"changed": {"lr": (0.1, 0.01)}, "deltas": {"val_loss": -0.2}}
log.log("base", 2, {"acc": 0.8})  → ValueError   steps must increase
log.log("nope", 1, {"acc": 0.8})  → KeyError
```

(`-0.2` is compared with a tolerance.)

## Constraints

- At most 1000 runs and 10 000 logged steps per run.
- Plain Python only.

## Hints

1. What does one run need to hold, and what container keeps runs in the order they were started?
2. If you store the caller's `config` dict directly, what happens when they reuse and edit it for the next run?
3. For `best`, how can one pass over runs and steps, with a strict comparison, give you the tie-breaking rule for free?
4. For `compare`, which set operation gives you every config key that either run has, and which gives the metrics both have?

## Explain-back

- Two runs differ in learning rate, but you also edited the data loader between them and didn't record it. What can you conclude from their difference, and which field of the record would have saved you?
- Why record per-step metrics rather than only the final number?
- Why is one seed per config not enough to call one config better than another?
- Why must every run you compare be scored on the same validation split?
