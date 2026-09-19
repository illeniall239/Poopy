# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from collections import deque


def topo_sort(graph: dict[str, list[str]]) -> list[str]:
    # Kahn's algorithm: repeatedly place a node that nothing unplaced points to.
    edges = {u: list(dict.fromkeys(vs)) for u, vs in graph.items()}  # duplicate edges are one constraint
    nodes = list(dict.fromkeys([*edges, *(v for vs in edges.values() for v in vs)]))
    indegree = {n: 0 for n in nodes}
    for vs in edges.values():
        for v in vs:
            indegree[v] += 1

    ready = deque(n for n in nodes if indegree[n] == 0)
    order = []
    while ready:
        u = ready.popleft()
        order.append(u)
        for v in edges.get(u, []):
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)

    if len(order) != len(nodes):
        raise ValueError("graph has a cycle")
    return order
