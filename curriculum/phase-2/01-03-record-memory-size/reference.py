# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
SIZES = {"bool": 1, "i8": 1, "i16": 2, "i32": 4, "f32": 4, "i64": 8, "f64": 8, "ptr": 8}


def _round_up(offset: int, multiple: int) -> int:
    return -(-offset // multiple) * multiple


def record_size(fields: list[str]) -> int:
    offset = 0
    largest = 1
    for field in fields:
        size = SIZES[field]
        offset = _round_up(offset, size) + size
        largest = max(largest, size)
    return _round_up(offset, largest)


def array_size(fields: list[str], count: int) -> int:
    return record_size(fields) * count
