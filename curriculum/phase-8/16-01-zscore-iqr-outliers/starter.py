def zscore_flags(xs: list[float], k: float = 3.0) -> list[bool]:
    """Flag values whose population z-score magnitude is strictly above k; ValueError if empty."""
    raise NotImplementedError


def iqr_flags(xs: list[float], factor: float = 1.5) -> list[bool]:
    """Flag values strictly outside [Q1 - factor*IQR, Q3 + factor*IQR]; ValueError if empty."""
    raise NotImplementedError
