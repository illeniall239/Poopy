from typing import Union

Nested = Union[int, list["Nested"]]


def flatten(items: list[Nested]) -> list[int]:
    """Return a new flat list of every number in items, left to right."""
    raise NotImplementedError


def depth(items: list[Nested]) -> int:
    """Return the nesting depth: 1 for a flat list, 1 + the deepest inner list otherwise."""
    raise NotImplementedError
