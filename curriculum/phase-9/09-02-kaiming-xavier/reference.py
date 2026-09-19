# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def kaiming_std(fan_in: int, gain: float) -> float:
    if fan_in < 1 or gain <= 0:
        raise ValueError("need fan_in >= 1 and gain > 0")
    return gain / math.sqrt(fan_in)


def xavier_bound(fan_in: int, fan_out: int) -> float:
    if fan_in < 1 or fan_out < 1:
        raise ValueError("fans must be >= 1")
    return math.sqrt(6.0 / (fan_in + fan_out))
