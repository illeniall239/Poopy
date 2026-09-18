# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def pair_with_target_sum(values: list[int], target: int) -> list[int]:
    first_index_of: dict[int, int] = {}
    for j, value in enumerate(values):
        i = first_index_of.get(target - value)
        if i is not None:
            return [i, j]
        first_index_of.setdefault(value, j)
    return [-1, -1]
