import { test } from "node:test";
import assert from "node:assert/strict";
import { ListNode, middleNode, hasCycle } from "./solution.ts";

// Builds nodes 0..count-1 holding `values`; if loopTo >= 0, the last node points back to nodes[loopTo].
function nodesOf(values: number[], loopTo = -1): ListNode[] {
  const nodes = values.map((v) => new ListNode(v));
  for (let i = 0; i + 1 < nodes.length; i++) nodes[i].next = nodes[i + 1];
  if (loopTo >= 0) nodes[nodes.length - 1].next = nodes[loopTo];
  return nodes;
}

function range(n: number): number[] {
  return Array.from({ length: n }, (_, i) => i + 1);
}

test("middle of an odd-length list", () => {
  const nodes = nodesOf([1, 2, 3, 4, 5]);
  assert.equal(middleNode(nodes[0]), nodes[2]);
});

test("middle of an even-length list is the second middle node", () => {
  const nodes = nodesOf([1, 2, 3, 4, 5, 6]);
  assert.equal(middleNode(nodes[0]), nodes[3]);
  const two = nodesOf([1, 2]);
  assert.equal(middleNode(two[0]), two[1]);
});

test("middle of one node and of an empty list", () => {
  const one = nodesOf([9]);
  assert.equal(middleNode(one[0]), one[0]);
  assert.equal(middleNode(null), null);
});

test("list ending in null has no cycle", () => {
  assert.equal(hasCycle(nodesOf([1, 2, 3, 4])[0]), false);
  assert.equal(hasCycle(nodesOf([1])[0]), false);
  assert.equal(hasCycle(null), false);
});

test("last node pointing back into the list is a cycle", () => {
  assert.equal(hasCycle(nodesOf([1, 2, 3, 4], 1)[0]), true);
  assert.equal(hasCycle(nodesOf([1, 2, 3, 4], 0)[0]), true);
  assert.equal(hasCycle(nodesOf([1, 2], 1)[0]), true);
});

test("a node pointing to itself is a cycle", () => {
  assert.equal(hasCycle(nodesOf([7], 0)[0]), true);
});

test("neither function changes the nodes", () => {
  const nodes = nodesOf([5, 6, 7, 8], 2);
  hasCycle(nodes[0]);
  const plain = nodesOf([1, 2, 3]);
  middleNode(plain[0]);
  assert.deepEqual(nodes.map((n) => [n.val, n.next]), [[5, nodes[1]], [6, nodes[2]], [7, nodes[3]], [8, nodes[2]]]);
  assert.deepEqual(plain.map((n) => [n.val, n.next]), [[1, plain[1]], [2, plain[2]], [3, null]]);
});

test("1000000 nodes in O(n)", () => {
  const n = 1000000;
  const nodes = nodesOf(range(n));
  assert.equal(middleNode(nodes[0]), nodes[n / 2]);
  assert.equal(hasCycle(nodes[0]), false);
  nodes[n - 1].next = nodes[n / 2];
  assert.equal(hasCycle(nodes[0]), true);
});
