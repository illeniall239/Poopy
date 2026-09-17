from typing import Callable, TypeVar

T = TypeVar("T")


def group_by(items: list[T], key_of: Callable[[T], str]) -> dict[str, list[T]]:
    """Group items by key_of(item), keeping input order within each group."""
    raise NotImplementedError
