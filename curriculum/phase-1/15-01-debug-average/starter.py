from typing import Optional


def average(numbers: list[float]) -> Optional[float]:
    if len(numbers) == 0:
        return None
    total = 0
    for i in range(1, len(numbers)):
        total += numbers[i]
    return round(total / len(numbers))
