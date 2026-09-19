# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def diagnose(human: float, train: float, train_dev: float, dev: float, test: float) -> str:
    errors = [human, train, train_dev, dev, test]
    if any(not 0.0 <= e <= 1.0 for e in errors):
        raise ValueError("error rates must be in [0, 1]")
    gaps = [
        ("avoidable bias", train - human),
        ("variance", train_dev - train),
        ("data mismatch", dev - train_dev),
        ("dev overfitting", test - dev),
    ]
    best_name, best_gap = gaps[0]
    for name, gap in gaps[1:]:
        if gap > best_gap + 1e-9:  # a later gap must win clearly; near-ties keep the earlier one
            best_name, best_gap = name, gap
    return best_name
