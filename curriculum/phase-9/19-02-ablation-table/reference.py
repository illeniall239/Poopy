# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def ablation_table(runs: list[dict], baseline: str) -> list[dict]:
    by_name = {}
    for run in runs:
        if run["name"] in by_name:
            raise ValueError(f"duplicate run name {run['name']!r}")
        by_name[run["name"]] = run
    if baseline not in by_name:
        raise ValueError(f"no run named {baseline!r}")
    base = by_name[baseline]

    table = []
    for run in runs:
        if run["name"] == baseline:
            continue
        missing = base["metrics"].keys() - run["metrics"].keys()
        if missing:
            raise ValueError(f"run {run['name']!r} is missing metrics {sorted(missing)}")
        table.append({
            "name": run["name"],
            "deltas": {m: run["metrics"][m] - v for m, v in base["metrics"].items()},
            "seed_differs": run["seed"] != base["seed"],
        })
    return table
