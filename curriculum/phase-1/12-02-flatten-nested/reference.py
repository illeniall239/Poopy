# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Union

Nested = Union[int, list["Nested"]]


def flatten(items: list[Nested]) -> list[int]:
    result: list[int] = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def depth(items: list[Nested]) -> int:
    deepest_inner = 0
    for item in items:
        if isinstance(item, list):
            deepest_inner = max(deepest_inner, depth(item))
    return 1 + deepest_inner
