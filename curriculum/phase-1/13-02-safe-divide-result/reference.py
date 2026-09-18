# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
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
    if not math.isfinite(a) or not math.isfinite(b):
        return {"ok": False, "error": "Inputs must be finite numbers"}
    if b == 0:
        return {"ok": False, "error": "Cannot divide by zero"}
    return {"ok": True, "value": a / b}


def sum_of_quotients(pairs: list[Pair]) -> Result:
    total = 0.0
    for i, pair in enumerate(pairs, start=1):
        result = safe_divide(pair["a"], pair["b"])
        if not result["ok"]:
            return {"ok": False, "error": f"Pair {i}: {result['error']}"}
        total += result["value"]
    return {"ok": True, "value": total}
