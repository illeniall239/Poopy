# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Optional


def average(numbers: list[float]) -> Optional[float]:
    if len(numbers) == 0:
        return None
    total = 0
    for i in range(0, len(numbers)):
        total += numbers[i]
    return total / len(numbers)
