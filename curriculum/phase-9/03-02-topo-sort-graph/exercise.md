# Topological order of a graph

Topic: 3. Computational graphs and backprop by hand
Difficulty: 2 of 3

## Problem

Backprop may only process a node once every node that uses it has already passed its gradient back. That order is the reverse of a **topological order**: an order in which every node comes before all the nodes it feeds into.

Write `topo_sort(graph)` in plain Python. `graph` is a dict mapping each node (a string) to the list of nodes it has an edge **to**: `{"a": ["c"]}` means `a → c`, so `a` must come before `c`. A node may appear only as a target and never as a key; it is still part of the graph. A node may list the same target twice (like `x * x` using `x` twice); that is still just the constraint "before that target".

Return a list containing every node exactly once, such that for every edge `u → v`, `u` appears before `v`. When several orders are valid, any of them is accepted.

Raise `ValueError` if the graph contains a cycle, including a node with an edge to itself.

## Examples

```
topo_sort({"a": ["c"], "b": ["c"], "c": ["d"]})   → ["a", "b", "c", "d"]   (or ["b", "a", "c", "d"])
topo_sort({"x": ["y", "y"]})                      → ["x", "y"]
topo_sort({"solo": []})                           → ["solo"]
topo_sort({})                                     → []
topo_sort({"a": ["b"], "b": ["a"]})               → ValueError
topo_sort({"a": ["a"]})                           → ValueError
```

## Constraints

- At most 500 nodes and 5 000 edges.
- Node names are strings.
- Plain Python only; do not import a graph library (or `graphlib`).

## Hints

1. Which nodes can safely go first in the order? How can you tell them apart from the others?
2. If you place a node and then pretend its outgoing edges are gone, which nodes become placeable next? (Or, with depth-first search: when is it safe to append a node, before or after visiting everything it points to?)
3. How do you make sure a node that only appears as a target is included?
4. If you run out of placeable nodes before every node is placed, what must the remaining nodes contain? With DFS, how would you notice you re-entered a node that is still "in progress"?

## Explain-back

- Backprop walks the topological order in reverse. What goes wrong if a node sends its gradient on before every node that uses it has contributed to its gradient?
- For `L = x * x + x`, `x` feeds two places. In what order must the three nodes be processed on the way back, and what happens at `x`?
- Why can a computational graph for one forward pass never contain a cycle? Where do recurrent networks' "loops" go?
