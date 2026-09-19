# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def _rates(metrics: dict, key: str) -> list[float]:
    if len(metrics) < 2:
        raise ValueError("need at least two groups to compare")
    rates = [m[key] for m in metrics.values()]
    if any(r is None for r in rates):
        raise ValueError(f"{key} is undefined for some group")
    return rates


def demographic_parity_difference(metrics: dict) -> float:
    rates = _rates(metrics, "selection_rate")
    return max(rates) - min(rates)


def equalized_odds_difference(metrics: dict) -> float:
    tprs = _rates(metrics, "tpr")
    fprs = _rates(metrics, "fpr")
    return max(max(tprs) - min(tprs), max(fprs) - min(fprs))


def disparate_impact_ratio(metrics: dict) -> float:
    rates = _rates(metrics, "selection_rate")
    if max(rates) == 0:
        return 1.0
    return min(rates) / max(rates)


def passes_four_fifths(metrics: dict) -> bool:
    return disparate_impact_ratio(metrics) >= 0.8 - 1e-9
