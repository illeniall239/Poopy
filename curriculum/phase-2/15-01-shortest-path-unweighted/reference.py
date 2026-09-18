# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from collections import deque


def shortest_path(n: int, edges: list[list[int]], start: int, end: int) -> int:
    neighbors: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    distance = [-1] * n
    distance[start] = 0
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == end:
            return distance[node]
        for nxt in neighbors[node]:
            if distance[nxt] == -1:
                distance[nxt] = distance[node] + 1
                queue.append(nxt)
    return -1
