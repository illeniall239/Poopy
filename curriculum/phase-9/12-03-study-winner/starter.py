from typing import Any, Hashable


def study_winner(runs: list[dict[str, Any]], scientific_param: str, metric: str) -> tuple[Hashable, dict[Hashable, float]]:
    """Return (best scientific value, {value: its best metric}) taking the best run over nuisance params."""
    raise NotImplementedError
