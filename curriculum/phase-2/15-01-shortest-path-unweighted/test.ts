import { test } from "node:test";
import assert from "node:assert/strict";
import { shortestPath } from "./solution.ts";

test("takes the shorter way round a cycle", () => {
  assert.equal(shortestPath(5, [[0, 1], [1, 2], [2, 3], [3, 4], [0, 4]], 0, 3), 2);
});

test("start equals end", () => {
  assert.equal(shortestPath(3, [[0, 1]], 2, 2), 0);
});

test("unreachable node gives -1", () => {
  assert.equal(shortestPath(4, [[0, 1], [2, 3]], 0, 3), -1);
});

test("node with no edges gives -1", () => {
  assert.equal(shortestPath(3, [], 0, 2), -1);
});

test("edges work in both directions", () => {
  assert.equal(shortestPath(3, [[1, 0], [2, 1]], 0, 2), 2);
});

test("cycles and repeated edges do not loop forever", () => {
  assert.equal(shortestPath(4, [[0, 1], [1, 2], [2, 0], [0, 1], [2, 3]], 0, 3), 2);
});

test("several routes of different lengths", () => {
  assert.equal(shortestPath(6, [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [4, 5], [1, 5]], 0, 5), 2);
});

test("path of 200 000 nodes in O(n + edges)", () => {
  const n = 200000;
  const edges: [number, number][] = [];
  for (let i = 0; i < n - 1; i++) {
    const p = (i * 7919) % (n - 1);
    edges.push(i % 2 === 0 ? [p, p + 1] : [p + 1, p]);
  }
  assert.equal(shortestPath(n, edges, 0, n - 1), n - 1);
});
