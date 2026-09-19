# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def kfold_indices(n: int, k: int) -> list[tuple[list[int], list[int]]]:
    if k < 2 or k > n:
        raise ValueError("need 2 <= k <= n")
    base, extra = divmod(n, k)
    folds = []
    start = 0
    for fold in range(k):
        size = base + (1 if fold < extra else 0)
        stop = start + size
        train = list(range(0, start)) + list(range(stop, n))
        folds.append((train, list(range(start, stop))))
        start = stop
    return folds
