from typing import Mapping, TypeVar

V = TypeVar("V")


def pick(obj: Mapping[str, V], keys: list[str]) -> dict[str, V]:
    """Return a new dict holding only the listed keys of obj."""
    raise NotImplementedError


def apply_patch(original: Mapping[str, V], patch: Mapping[str, V | None]) -> dict[str, V]:
    """Return a new dict: original overridden by patch, ignoring keys whose patch value is None."""
    raise NotImplementedError
