from dataclasses import dataclass
from typing import Callable


@dataclass
class Counter:
    increment: Callable[[], int]
    decrement: Callable[[], int]
    reset: Callable[[], int]
    value: Callable[[], int]


def make_counter(start: int = 0, step: int = 1) -> Counter:
    """Return a Counter whose four functions share one private count via a closure."""
    raise NotImplementedError
