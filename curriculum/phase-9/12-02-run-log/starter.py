from typing import Any


class RunLog:
    """A table of experiment runs: config, seed, code version and per-step metrics."""

    def __init__(self) -> None:
        """Start with no runs."""
        raise NotImplementedError

    def start(self, name: str, config: dict[str, Any], seed: int, code_version: str) -> None:
        """Record a new run with a copy of its config; ValueError on a duplicate name or reserved key."""
        raise NotImplementedError

    def log(self, name: str, step: int, metrics: dict[str, float]) -> None:
        """Record metrics for a run at a strictly increasing step."""
        raise NotImplementedError

    def best(self, metric: str, mode: str = "min") -> tuple[str, int, float]:
        """Return (run_name, step, value) of the best logged value of metric across all runs."""
        raise NotImplementedError

    def compare(self, a: str, b: str) -> dict[str, dict]:
        """Return {"changed": {key: (a_val, b_val)}, "deltas": {metric: last_b - last_a}}."""
        raise NotImplementedError
