def demographic_parity_difference(metrics: dict) -> float:
    """Largest selection rate minus the smallest across groups."""
    raise NotImplementedError


def equalized_odds_difference(metrics: dict) -> float:
    """Larger of the TPR spread and the FPR spread across groups; ValueError if any is None."""
    raise NotImplementedError


def disparate_impact_ratio(metrics: dict) -> float:
    """Smallest selection rate over the largest; 1.0 if all are 0."""
    raise NotImplementedError


def passes_four_fifths(metrics: dict) -> bool:
    """True when the disparate-impact ratio is at least 0.8 (with 1e-9 slack)."""
    raise NotImplementedError
