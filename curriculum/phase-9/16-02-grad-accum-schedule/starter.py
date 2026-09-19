def grad_accum_schedule(micro_batches: int, accum: int) -> tuple[list[int], float]:
    """Return (indices after which step() runs, loss scale per micro-batch)."""
    raise NotImplementedError
