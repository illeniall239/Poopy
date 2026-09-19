# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math

Record = tuple[str, list[str]]
ARITY = {"add": 2, "mul": 2, "tanh": 1}


def _topo_order(nodes: dict[str, Record]) -> list[str]:
    """Order the op nodes so each comes after the op nodes it reads (depth-first)."""
    order, done, in_progress = [], set(), set()

    def visit(name: str) -> None:
        if name in done or name not in nodes:  # leaves need no ordering
            return
        if name in in_progress:
            raise ValueError(f"cycle through {name!r}")
        in_progress.add(name)
        for inp in nodes[name][1]:
            visit(inp)
        in_progress.remove(name)
        done.add(name)
        order.append(name)

    for name in nodes:
        visit(name)
    return order


def graph_backward(
    nodes: dict[str, Record], leaves: dict[str, float], output: str
) -> tuple[dict[str, float], dict[str, float]]:
    if set(nodes) & set(leaves):
        raise ValueError("a name cannot be both a leaf and a node")
    for name, (op, inputs) in nodes.items():
        if op not in ARITY:
            raise ValueError(f"unknown op {op!r}")
        if len(inputs) != ARITY[op]:
            raise ValueError(f"{op} takes {ARITY[op]} inputs, got {len(inputs)}")
        for inp in inputs:
            if inp not in nodes and inp not in leaves:
                raise ValueError(f"unknown input {inp!r}")
    if output not in nodes and output not in leaves:
        raise ValueError(f"unknown output {output!r}")

    order = _topo_order(nodes)

    values = {name: float(v) for name, v in leaves.items()}
    for name in order:
        op, inputs = nodes[name]
        xs = [values[i] for i in inputs]
        if op == "add":
            values[name] = xs[0] + xs[1]
        elif op == "mul":
            values[name] = xs[0] * xs[1]
        else:
            values[name] = math.tanh(xs[0])

    grads = {name: 0.0 for name in values}
    grads[output] = 1.0
    for name in reversed(order):  # every consumer of `name` has already added into grads[name]
        op, inputs = nodes[name]
        up = grads[name]
        if op == "add":
            grads[inputs[0]] += up
            grads[inputs[1]] += up
        elif op == "mul":
            a, b = inputs
            grads[a] += up * values[b]  # += : a and b may be the same name
            grads[b] += up * values[a]
        else:
            grads[inputs[0]] += up * (1.0 - values[name] ** 2)
    return values, grads
