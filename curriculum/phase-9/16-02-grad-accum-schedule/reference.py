# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def grad_accum_schedule(micro_batches: int, accum: int) -> tuple[list[int], float]:
    if micro_batches < 1 or accum < 1:
        raise ValueError("micro_batches and accum must be at least 1")
    step_at = [i for i in range(micro_batches) if (i + 1) % accum == 0 or i == micro_batches - 1]
    return step_at, 1.0 / accum
