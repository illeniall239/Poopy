def kaiming_std(fan_in: int, gain: float) -> float:
    """Standard deviation of Kaiming normal init: gain / sqrt(fan_in)."""
    raise NotImplementedError


def xavier_bound(fan_in: int, fan_out: int) -> float:
    """Bound a of Xavier uniform init U(-a, a): sqrt(6 / (fan_in + fan_out))."""
    raise NotImplementedError
