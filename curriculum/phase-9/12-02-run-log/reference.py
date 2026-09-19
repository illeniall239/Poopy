# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Any


class RunLog:
    def __init__(self) -> None:
        self.runs: dict[str, dict[str, Any]] = {}  # insertion order = start order

    def start(self, name: str, config: dict[str, Any], seed: int, code_version: str) -> None:
        if name in self.runs:
            raise ValueError(f"run {name!r} already exists")
        if "seed" in config or "code_version" in config:
            raise ValueError("config may not use the reserved keys seed or code_version")
        self.runs[name] = {"config": dict(config), "seed": seed, "code_version": code_version, "steps": []}

    def log(self, name: str, step: int, metrics: dict[str, float]) -> None:
        steps = self.runs[name]["steps"]
        if steps and step <= steps[-1][0]:
            raise ValueError("steps must be strictly increasing")
        steps.append((step, dict(metrics)))

    def best(self, metric: str, mode: str = "min") -> tuple[str, int, float]:
        if mode not in ("min", "max"):
            raise ValueError("mode must be 'min' or 'max'")
        better = (lambda v, b: v < b) if mode == "min" else (lambda v, b: v > b)
        found = None
        for name, run in self.runs.items():
            for step, metrics in run["steps"]:
                if metric in metrics and (found is None or better(metrics[metric], found[2])):
                    found = (name, step, metrics[metric])
        if found is None:
            raise KeyError(metric)
        return found

    def _record(self, name: str) -> dict[str, Any]:
        run = self.runs[name]
        return {**run["config"], "seed": run["seed"], "code_version": run["code_version"]}

    def _last(self, name: str) -> dict[str, float]:
        last: dict[str, float] = {}
        for _, metrics in self.runs[name]["steps"]:
            last.update(metrics)
        return last

    def compare(self, a: str, b: str) -> dict[str, dict]:
        ra, rb = self._record(a), self._record(b)
        changed = {k: (ra.get(k), rb.get(k)) for k in ra.keys() | rb.keys() if ra.get(k) != rb.get(k)}
        la, lb = self._last(a), self._last(b)
        deltas = {m: lb[m] - la[m] for m in la.keys() & lb.keys()}
        return {"changed": changed, "deltas": deltas}
