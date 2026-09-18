# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def _reverse(values: list[int], start: int, end: int) -> None:
    while start < end:
        values[start], values[end] = values[end], values[start]
        start += 1
        end -= 1


def rotate_right(values: list[int], k: int) -> None:
    n = len(values)
    if n == 0:
        return
    steps = k % n
    _reverse(values, 0, n - 1)
    _reverse(values, 0, steps - 1)
    _reverse(values, steps, n - 1)
