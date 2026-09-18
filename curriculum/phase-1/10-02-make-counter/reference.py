# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from dataclasses import dataclass
from typing import Callable


@dataclass
class Counter:
    increment: Callable[[], int]
    decrement: Callable[[], int]
    reset: Callable[[], int]
    value: Callable[[], int]


def make_counter(start: int = 0, step: int = 1) -> Counter:
    count = start

    def increment() -> int:
        nonlocal count
        count += step
        return count

    def decrement() -> int:
        nonlocal count
        count -= step
        return count

    def reset() -> int:
        nonlocal count
        count = start
        return count

    def value() -> int:
        return count

    return Counter(increment=increment, decrement=decrement, reset=reset, value=value)
