# Shortest path in an unweighted graph

Topic: 15. Graphs
Difficulty: 1 of 3

## Problem

A graph has `n` nodes numbered `0` to `n - 1`. `edges` is an array of pairs `[a, b]`, each meaning there is an undirected edge between node `a` and node `b`: you can travel from `a` to `b` and from `b` to `a`. Every edge has the same length.

Write `shortestPath(n, edges, start, end)` that returns the fewest edges you must travel along to get from `start` to `end`, or `-1` if `end` cannot be reached. If `start` equals `end`, the answer is `0`.

Some nodes may have no edges at all, the graph may contain cycles, and the same edge may be listed twice.

## Examples

```
shortestPath(5, [[0, 1], [1, 2], [2, 3], [3, 4], [0, 4]], 0, 3)  → 2    (0 → 4 → 3)
shortestPath(4, [[0, 1], [2, 3]], 0, 3)                          → -1
shortestPath(3, [[0, 1]], 2, 2)                                  → 0
```

## Constraints

- 1 ≤ n ≤ 200 000; 0 ≤ `edges.length` ≤ 200 000; `0 ≤ start, end < n`.
- No edge connects a node to itself.
- O(n + edges.length) time and space. The tests include a path 200 000 nodes long (100 000 in Python), which is too deep for recursion and too slow if removing from the front of your queue costs O(n).

## Hints

1. How would you store the graph so that, given a node, you can list its neighbours without scanning all the edges? What must you remember about the direction of each edge?
2. If you explore every node one edge away from `start`, then every node two edges away, and so on, what do you know about the first time you reach `end`?
3. What stops you from walking around a cycle forever or putting the same node in line many times? At which moment should a node be marked: when you first discover it, or when you take it out to process it?
4. How can you know each node's distance when you take it out? Could you store it alongside the node, or process the line one "layer" at a time? How do you take items from the front of an array without making each removal O(n)?

## Explain-back

- Why does breadth-first search give the fewest edges, while depth-first search might not? Use the first example.
- Why do you mark a node visited when you add it to the queue rather than when you remove it? What goes wrong the other way?
- What are the time and space complexity in terms of the number of nodes and edges? Why is building the adjacency list part of that cost?
- What happens if you add each undirected edge in only one direction? Give an input where the answer changes.
