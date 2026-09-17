# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
from typing import Mapping, TypeVar

V = TypeVar("V")


def pick(obj: Mapping[str, V], keys: list[str]) -> dict[str, V]:
    return {key: obj[key] for key in keys}


def apply_patch(original: Mapping[str, V], patch: Mapping[str, V | None]) -> dict[str, V]:
    result = dict(original)
    for key, value in patch.items():
        if value is not None:
            result[key] = value
    return result
