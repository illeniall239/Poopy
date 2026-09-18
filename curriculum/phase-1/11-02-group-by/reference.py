# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Callable, TypeVar

T = TypeVar("T")


def group_by(items: list[T], key_of: Callable[[T], str]) -> dict[str, list[T]]:
    groups: dict[str, list[T]] = {}
    for item in items:
        groups.setdefault(key_of(item), []).append(item)
    return groups
