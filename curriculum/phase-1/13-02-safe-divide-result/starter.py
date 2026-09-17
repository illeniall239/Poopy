from typing import Literal, TypedDict, Union


class Ok(TypedDict):
    ok: Literal[True]
    value: float


class Err(TypedDict):
    ok: Literal[False]
    error: str


Result = Union[Ok, Err]


class Pair(TypedDict):
    a: float
    b: float


def safe_divide(a: float, b: float) -> Result:
    """Return {"ok": True, "value": a / b}, or {"ok": False, "error": ...} for non-finite inputs or b == 0."""
    raise NotImplementedError


def sum_of_quotients(pairs: list[Pair]) -> Result:
    """Return the sum of a / b over all pairs, or the first failure as "Pair <n>: <error>"."""
    raise NotImplementedError
