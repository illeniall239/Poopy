def ablation_table(runs: list[dict], baseline: str) -> list[dict]:
    """Return per-run metric deltas vs the named baseline, flagging runs whose seed differs."""
    raise NotImplementedError
