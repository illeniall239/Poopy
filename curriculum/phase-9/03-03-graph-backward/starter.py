Record = tuple[str, list[str]]


def graph_backward(
    nodes: dict[str, Record], leaves: dict[str, float], output: str
) -> tuple[dict[str, float], dict[str, float]]:
    """Return (values, grads) for every leaf and node: forward in topological order, backward in reverse."""
    raise NotImplementedError
